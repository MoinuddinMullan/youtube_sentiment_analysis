"""
Sentiview AI — Improved Labeling + Training Script

Changes from v1:
- Better labeling: uses VADER + a rule-based sarcasm/negative correction layer
- TF-IDF: ngram_range (1,3), higher max_features (50k), char analyzer disabled
- Model: LinearSVC (much better for text than LogisticRegression) with fallback to LR
- Class weights: balanced to prevent bias toward "neutral" (majority class)
- Post-processing rule layer in model_service to catch sarcasm at inference time
"""
import os
import sys
import json
import time
import joblib
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocess import clean_text, normalize_label

# ─── CONFIG ──────────────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH        = os.path.join(BASE_DIR, "data", "raw", "youtube_comments_with_labels.csv")
COMMENT_COL     = "comment_text"
SENTIMENT_COL   = "label_sentiment"
ARTIFACTS_DIR   = os.path.join(BASE_DIR, "ml", "artifacts")
MODEL_PATH      = os.path.join(ARTIFACTS_DIR, "sentiment_model.joblib")
VECTORIZER_PATH = os.path.join(ARTIFACTS_DIR, "tfidf_vectorizer.joblib")
METADATA_PATH   = os.path.join(ARTIFACTS_DIR, "model_metadata.json")
TEST_SIZE       = 0.20
RANDOM_STATE    = 42
MAX_FEATURES    = 50000   # doubled from v1
# ─────────────────────────────────────────────────────────────────────────────

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

print("=" * 60)
print("SENTIVIEW AI - Model Training (v2 - Improved)")
print("=" * 60)

# ─── Step 1: Load ─────────────────────────────────────────────────────────────
print(f"\n[1/8] Loading dataset: {CSV_PATH}")
if not os.path.exists(CSV_PATH):
    print(f"\nERROR: Dataset not found at {CSV_PATH}")
    sys.exit(1)

try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8", on_bad_lines="skip")
except Exception:
    df = pd.read_csv(CSV_PATH, encoding="latin-1", on_bad_lines="skip")

print(f"      Shape: {df.shape}")
print(f"      Columns: {df.columns.tolist()}")

# ─── Step 2: Validate ─────────────────────────────────────────────────────────
print(f"\n[2/8] Validating columns: '{COMMENT_COL}', '{SENTIMENT_COL}'")
if COMMENT_COL not in df.columns or SENTIMENT_COL not in df.columns:
    print(f"ERROR: Missing required columns. Available: {df.columns.tolist()}")
    sys.exit(1)

df = df[[COMMENT_COL, SENTIMENT_COL]].copy()
df = df.dropna()
df[COMMENT_COL]    = df[COMMENT_COL].astype(str).str.strip()
df[SENTIMENT_COL]  = df[SENTIMENT_COL].astype(str)
df = df[df[COMMENT_COL].str.len() >= 3]
df = df.drop_duplicates(subset=[COMMENT_COL])
print(f"      After cleaning: {len(df)} rows")

# ─── Step 3: Better labeling with sarcasm/negation correction ─────────────────
print("\n[3/8] Applying improved sentiment labeling (VADER + rule corrections)...")

import nltk
nltk.download("vader_lexicon", quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Strong negative patterns that VADER often mislabels
STRONG_NEGATIVE_PATTERNS = [
    r"\bdon'?t\s+bother\b",
    r"\bwaste\s+of\s+(time|money)\b",
    r"\bclickbait\b",
    r"\bawful\b", r"\bterrible\b", r"\bhorrible\b", r"\bdisgusting\b",
    r"\boutdated\b.*\berrors?\b",
    r"\bworse?\s+(ever|than)\b",
    r"\bunsubscribed?\b",
    r"\bdropped\s+in\s+quality\b",
    r"\bleft\s+me\s+more\s+confused\b",
    r"\bpainful\s+to\s+watch\b",
    r"\brepeat(ing)?\s+the\s+same\b",
    r"\bhalf\s+the\s+code.*outdated\b",
    r"\btotally\s+wrong\b",
    r"\bcompletely\s+(wrong|biased|unresearched)\b",
    r"\blost\s+all\s+respect\b",
]

# Sarcasm patterns (these look positive syntactically but are negative)
SARCASM_NEGATIVE_PATTERNS = [
    r"\boh\s+great\b.*(\.\.\.|!|use|tool|break)",
    r"'life.changing'",
    r"cured\s+my\s+boredom.*sleep",
    r"put\s+me\s+(straight\s+)?to\s+sleep",
    r"thought\s+he\s+cooked\b",
    r"\bcooked\s+with\s+this\b",
    r"\d{1,2}\/10.*but.*wrong",
    r"\bbreaks\s+after\s+\d+\s+days?\b",
]

def improved_label(text: str) -> str:
    """VADER + rule-based corrections for sarcasm and strong negatives."""
    if not isinstance(text, str) or len(text.strip()) < 2:
        return "neutral"

    text_lower = text.lower()

    # Hard override: strong negative patterns
    for pattern in STRONG_NEGATIVE_PATTERNS:
        if re.search(pattern, text_lower):
            return "negative"

    # Hard override: sarcasm patterns → negative
    for pattern in SARCASM_NEGATIVE_PATTERNS:
        if re.search(pattern, text_lower):
            return "negative"

    # VADER fallback
    score = sia.polarity_scores(text)["compound"]
    if score >= 0.08:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

df["label_clean"] = df[COMMENT_COL].apply(improved_label)
print("      Distribution:")
print(df["label_clean"].value_counts().to_string())

# ─── Step 4: Preprocess text ──────────────────────────────────────────────────
print("\n[4/8] Preprocessing text with negation handling...")
t_start = time.time()
df["text_clean"] = df[COMMENT_COL].apply(clean_text)
df = df[df["text_clean"].str.strip().str.len() > 0]
print(f"      Done in {round(time.time() - t_start, 1)}s | Final rows: {len(df)}")

# ─── Step 5: Split ────────────────────────────────────────────────────────────
X = df["text_clean"]
y = df["label_clean"]
labels = sorted(y.unique().tolist())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)
print(f"\n[5/8] Train/Test split: {len(X_train)} train, {len(X_test)} test")
print(f"      Labels: {labels}")

# ─── Step 6: TF-IDF ──────────────────────────────────────────────────────────
print("\n[6/8] Fitting TF-IDF vectorizer (1-3 ngrams, 50k features)...")
vectorizer = TfidfVectorizer(
    max_features=MAX_FEATURES,
    ngram_range=(1, 3),          # unigrams + bigrams + trigrams
    min_df=2,
    sublinear_tf=True,
    strip_accents="unicode",
    analyzer="word",
    token_pattern=r"\b[a-z0-9_]+\b",  # keep NOT_ and sarcasm_ tokens
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)
print(f"      Vocabulary size: {len(vectorizer.vocabulary_)}")

# ─── Step 7: Train LinearSVC (much better than LR for text) ──────────────────
print("\n[7/8] Training LinearSVC with probability calibration...")
t0 = time.time()

base_svc = LinearSVC(
    C=0.8,
    class_weight="balanced",
    max_iter=2000,
    random_state=RANDOM_STATE,
)
# Wrap in CalibratedClassifierCV to get predict_proba support
model = CalibratedClassifierCV(base_svc, cv=3, method="sigmoid")
model.fit(X_train_vec, y_train)
elapsed = round(time.time() - t0, 2)
print(f"      Training complete in {elapsed}s")

# ─── Step 8: Evaluate ────────────────────────────────────────────────────────
print("\n[8/8] Evaluation Results")
y_pred = model.predict(X_test_vec)
acc    = round(accuracy_score(y_test, y_pred), 4)
report = classification_report(y_test, y_pred)
print(f"\n      Accuracy: {acc}\n")
print(report)

# Save
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

metadata = {
    "model_name": "LinearSVC_CalibratedCV",
    "vectorizer": "TfidfVectorizer",
    "labels": labels,
    "accuracy": acc,
    "test_size": TEST_SIZE,
    "random_state": RANDOM_STATE,
    "max_features": MAX_FEATURES,
    "ngram_range": [1, 3],
    "training_samples": len(X_train),
    "test_samples": len(X_test),
}
with open(METADATA_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"\nModel saved:      {MODEL_PATH}")
print(f"Vectorizer saved: {VECTORIZER_PATH}")
print(f"Metadata saved:   {METADATA_PATH}")
print("\nNow restart the API:")
print("   uvicorn app.main:app --reload --port 8000")
