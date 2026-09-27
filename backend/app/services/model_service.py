import joblib
import json
import re
import numpy as np
from typing import Optional
from ..config import settings
from .preprocessing import clean_text

# ─── Hard-rule overrides (applied AFTER model prediction) ────────────────────
# These catch sarcasm / strong-negatives that even a good model can miss.
_HARD_NEGATIVE_RULES = [
    r"\bdon'?t\s+bother\b",
    r"\bwaste\s+of\s+(time|money)\b",
    r"\bclickbait\b",
    r"\bpainful\s+to\s+watch\b",
    r"\bleft\s+me\s+more\s+confused\b",
    r"\bunsubscribed?\b",
    r"\bworst\s+(ever|video|channel|explanation)\b",
    r"\boutdated\b.*\b(error|wrong|broken)\b",
    r"\bdropped\s+in\s+quality\b",
    r"\blost\s+all\s+respect\b",
    r"\bcompletely\s+(wrong|biased|misleading|unresearched)\b",
    r"\btotally\s+wrong\b",
    r"\boh\s+great\b.{0,40}(break|use|tool|two\s+days?)",
    r"cured\s+my\s+boredom",
    r"put\s+me\s+(straight\s+)?to\s+sleep",
    r"putting\s+me\s+(straight\s+)?to\s+sleep",
    r"'life.changing'.{0,20}(break|after|days?)",
    r"\bthought\s+he\s+cooked\b",
    r"\bcooked\s+with\s+this\b",
    r"\bbreaks\s+after\s+\d+\s+days?\b",
    r"\bhalf\s+the\s+code.{0,20}(outdated|wrong|error)",
    # Sarcasm: spending too long on something simple
    r"\bspent\s+\d+\s+minutes?\b.{0,50}\bcould\s+have\b",
    r"\bcould\s+have\s+been\s+said\s+in\s+\d+\s+seconds?\b",
    r"\b\d+\s+minutes?.{0,30}(could have been|explaining something that could)\b",
    r"\bnot\s+worth\s+(all\s+the\s+hype|the\s+hype|watching)\b",
    # Skip-to-bypass complaints (e.g. "skip to 8:00 to bypass the sponsor segment")
    r"\bskip\s+to\b.{0,50}(bypass|self.?promotion|sponsor)",
    r"\bendless\s+(self.?promotion|ads?|sponsor)\b",
    # Emoji-based (post-clean tokens)
    r"skull_emoji_lol",
    r"eye_roll_emoji",
    r"boring_sleep_emoji",
    r"facepalm_emoji",
]

# "Not terrible but not worth" type comments → force NEUTRAL not negative
_HARD_NEUTRAL_RULES = [
    r"\bnot\s+(terrible|bad)\b.{0,40}\bnot\s+worth\b",
    r"\bi\s+mean.{0,20}\bnot\s+terrible\b",
    r"\bnot\s+bad\b.{0,30}\bnot\s+great\b",
]

_HARD_POSITIVE_RULES = [
    r"\babsolute\s+masterpiece\b",
    r"\bdeserve\s+millions?\s+of\s+views\b",
    r"\bsubscribed\s+immediately\b",
    r"\bquality\s+of\s+(editing|content).{0,20}\b(insane|amazing|incredible|great)\b",
    r"\bpacing\s+in\s+this\s+video\s+is\s+(insane|amazing|incredible)\b",
    # "doesn't waste time" = positive (negation of waste is good)
    r"\bdoesn'?t\s+waste\b.{0,30}\b(time|minutes?)\b",
    r"direct\s+to\s+the\s+point",
    r"fire_great_emoji",
    r"clapping_great_emoji",
    r"\blife\s+changing\b",
    r"\bchanged\s+my\s+(perspective|life|mind)\b",
    r"\bthanks?\s+for\s+(explaining|teaching|making)\b",
]


def _apply_hard_rules(original_text: str, predicted: str, probabilities: dict) -> tuple[str, float]:
    """
    Apply hard rule overrides on the ORIGINAL text (before cleaning).
    Priority: NEUTRAL → NEGATIVE → POSITIVE → model prediction.
    Returns (corrected_sentiment, corrected_confidence).
    """
    text_lower = original_text.lower()
    cleaned = clean_text(original_text)

    # 1. NEUTRAL overrides checked FIRST — prevents false-negative on mixed-sentiment comments
    for pattern in _HARD_NEUTRAL_RULES:
        if re.search(pattern, text_lower) or re.search(pattern, cleaned):
            return "neutral", max(0.65, probabilities.get("neutral", 0.40))

    # 2. NEGATIVE overrides
    for pattern in _HARD_NEGATIVE_RULES:
        if re.search(pattern, text_lower) or re.search(pattern, cleaned):
            return "negative", max(0.75, probabilities.get("negative", 0.50))

    # 3. POSITIVE overrides
    for pattern in _HARD_POSITIVE_RULES:
        if re.search(pattern, text_lower) or re.search(pattern, cleaned):
            return "positive", max(0.80, probabilities.get("positive", 0.50))

    # 4. Fall through to raw model prediction
    return predicted, max(probabilities.values())


class ModelService:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.metadata = None
        self.labels = ["negative", "neutral", "positive"]
        self.is_loaded = False

    def load_model(self):
        """Load the trained model and vectorizer from disk."""
        try:
            self.model      = joblib.load(settings.MODEL_PATH)
            self.vectorizer = joblib.load(settings.VECTORIZER_PATH)
            with open(settings.METADATA_PATH, "r") as f:
                self.metadata = json.load(f)
            self.labels     = self.metadata.get("labels", self.labels)
            self.is_loaded  = True
            print(f"Model loaded: {self.metadata.get('model_name')} | Accuracy: {self.metadata.get('accuracy')}")
        except FileNotFoundError as e:
            print(f"Model artifacts not found: {e}")
            print("   Run: cd backend && python ml/train.py")
            self.is_loaded = False
        except Exception as e:
            print(f"Model loading error: {e}")
            self.is_loaded = False

    def predict_single(self, text: str) -> dict:
        """Predict sentiment for a single text with rule-override layer."""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Run: cd backend && python ml/train.py")

        cleaned      = clean_text(text)
        vec          = self.vectorizer.transform([cleaned])
        raw_pred     = self.model.predict(vec)[0]
        raw_probs    = self.model.predict_proba(vec)[0]

        prob_dict = {
            label: round(float(p), 4)
            for label, p in zip(self.labels, raw_probs)
        }

        # Apply hard rules as safety net
        final_pred, final_conf = _apply_hard_rules(text, raw_pred, prob_dict)

        return {
            "sentiment":    str(final_pred),
            "confidence":   round(float(final_conf), 4),
            "probabilities": prob_dict,
        }

    def predict_batch(self, texts: list) -> list:
        """Predict sentiment for a batch of texts with rule-override layer."""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Run: cd backend && python ml/train.py")

        if not texts:
            return []

        cleaned_texts = [clean_text(t) for t in texts]
        vecs          = self.vectorizer.transform(cleaned_texts)
        predictions   = self.model.predict(vecs)
        all_probs     = self.model.predict_proba(vecs)

        results = []
        for original, pred, probs in zip(texts, predictions, all_probs):
            prob_dict = {
                label: round(float(p), 4)
                for label, p in zip(self.labels, probs)
            }
            final_pred, final_conf = _apply_hard_rules(original, pred, prob_dict)
            results.append({
                "text":          original,
                "sentiment":     str(final_pred),
                "confidence":    round(float(final_conf), 4),
                "probabilities": prob_dict,
            })

        return results


# Global singleton
model_service = ModelService()
