"""
Sentiview AI — Model Evaluation Script
Usage: python ml/evaluate.py
"""
import os
import sys
import json
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocess import clean_text, normalize_label

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS_DIR   = os.path.join(BASE_DIR, "ml", "artifacts")
MODEL_PATH      = os.path.join(ARTIFACTS_DIR, "sentiment_model.joblib")
VECTORIZER_PATH = os.path.join(ARTIFACTS_DIR, "tfidf_vectorizer.joblib")
METADATA_PATH   = os.path.join(ARTIFACTS_DIR, "model_metadata.json")
CSV_PATH        = os.path.join(BASE_DIR, "data", "raw", "youtube_comments.csv")

if not os.path.exists(MODEL_PATH):
    print("❌ No model found. Run: python ml/train.py")
    sys.exit(1)

print("Loading model artifacts...")
model      = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
with open(METADATA_PATH) as f:
    metadata = json.load(f)

print(f"Model: {metadata['model_name']}")
print(f"Training accuracy: {metadata['accuracy']}")
print(f"Labels: {metadata['labels']}")

# Quick test
test_comments = [
    "This video is absolutely amazing! Best content ever!",
    "Meh, it was okay I guess",
    "This is terrible, waste of time",
    "Really informative, learned a lot!",
    "Not sure how I feel about this..."
]

print("\n--- Quick Test Predictions ---")
cleaned = [clean_text(c) for c in test_comments]
vecs    = vectorizer.transform(cleaned)
preds   = model.predict(vecs)
probs   = model.predict_proba(vecs)

for comment, pred, prob in zip(test_comments, preds, probs):
    conf = max(prob)
    print(f"  [{pred.upper():8s}] ({conf:.2%}) — {comment[:60]}")

print("\n✅ Model evaluation complete")
