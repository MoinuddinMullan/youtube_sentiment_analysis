"""
Sentiview AI — API-side preprocessing (mirrors ml/preprocess.py exactly).
This is used by model_service.py at inference time.
"""
import re
from typing import Optional

# ─── Emoji text map ──────────────────────────────────────────────────────────
EMOJI_MAP = {
    "🙄": " eye_roll_emoji ",
    "💀": " skull_emoji_lol ",
    "😂": " laughing_emoji ",
    "😭": " crying_emoji ",
    "🤣": " laughing_emoji ",
    "😡": " angry_emoji ",
    "👎": " thumbs_down_emoji ",
    "👍": " thumbs_up_emoji ",
    "❤️": " heart_emoji ",
    "😍": " love_emoji ",
    "🔥": " fire_great_emoji ",
    "✅": " checkmark_good_emoji ",
    "❌": " cross_bad_emoji ",
    "😤": " frustrated_emoji ",
    "🤦": " facepalm_emoji ",
    "🤮": " disgusting_emoji ",
    "😴": " boring_sleep_emoji ",
    "🥱": " boring_sleep_emoji ",
    "🎉": " celebrate_emoji ",
    "👏": " clapping_great_emoji ",
    "😎": " cool_emoji ",
    "😒": " unimpressed_emoji ",
    "🤦‍♂️": " facepalm_emoji ",
    "🤦‍♀️": " facepalm_emoji ",
}

# ─── Negation words ──────────────────────────────────────────────────────────
NEGATION_WORDS = {
    "not", "no", "never", "neither", "nor", "none",
    "don't", "dont", "doesn't", "doesnt", "didn't", "didnt",
    "can't", "cant", "couldn't", "couldnt", "won't", "wont",
    "wouldn't", "wouldnt", "isn't", "isnt", "aren't", "arent",
    "wasn't", "wasnt", "weren't", "werent", "haven't", "havent",
    "hasn't", "hasnt", "hadn't", "hadnt", "shouldn't", "shouldnt",
    "without", "barely", "hardly", "scarcely",
}

# ─── Sarcasm / Irony patterns ─────────────────────────────────────────────────
SARCASM_PATTERNS = [
    (r"\boh\s+(great|wow|sure|perfect|wonderful|fantastic|amazing)\b", " sarcasm_oh_great "),
    (r"\banother\s+\S+\s+that\s+", " sarcasm_another_that "),
    (r"'(amazing|great|life.changing|genius|expert|perfect)'", r" sarcasm_quoted "),
    (r"\.{2,}", " ellipsis_sarcasm "),
    (r"\b(10\/10|perfect|flawless|masterpiece)\b.{0,30}\b(but|however|except|although|yet)\b",
     " praise_contradiction "),
]


def _replace_emojis(text: str) -> str:
    for emoji, replacement in EMOJI_MAP.items():
        text = text.replace(emoji, replacement)
    return text


def _apply_sarcasm_patterns(text: str) -> str:
    for pattern, replacement in SARCASM_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def _handle_negation(tokens: list) -> list:
    result = []
    negate = 0
    for token in tokens:
        if token in NEGATION_WORDS:
            negate = 4
            result.append(token)
        elif negate > 0:
            result.append(f"NOT_{token}")
            negate -= 1
            if token in {",", ".", "!", "?", ";", "but", "however"}:
                negate = 0
        else:
            result.append(token)
    return result


def clean_text(text: str) -> str:
    """
    Full NLP preprocessing pipeline — identical to ml/preprocess.py.
    1. Emoji → descriptive text
    2. Tag sarcasm patterns
    3. Remove URLs + HTML
    4. Lowercase
    5. Tokenise + negation handling
    6. Strip noise chars (keep underscores for special tokens)
    7. Collapse whitespace
    """
    if not isinstance(text, str):
        text = str(text)

    text = _replace_emojis(text)
    text = _apply_sarcasm_patterns(text)

    text = re.sub(r"http\S+|www\S+|https\S+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"<.*?>", " ", text)

    text = text.lower()

    tokens = text.split()
    tokens = _handle_negation(tokens)
    text = " ".join(tokens)

    text = re.sub(r"[^a-z0-9_\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def is_valid_comment(text: str) -> bool:
    """Check if a comment is valid for analysis."""
    if not text or not isinstance(text, str):
        return False
    return len(text.strip()) >= 2
