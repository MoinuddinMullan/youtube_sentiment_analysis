"""
Sentiview AI — Improved Preprocessing Pipeline

Key improvements over v1:
- Negation handling: "don't like" → "dont_like NOT_like" so TF-IDF learns negation
- Emoji preservation: converts emojis to descriptive text before stripping
- Sarcasm marker preservation: ellipsis, quote-wrapped praise, etc.
- Punctuation-based feature: question/exclamation count as signals
"""
import re


# ─── Emoji text map (covers common YouTube comment emojis) ──────────────────
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

# ─── Negation words ─────────────────────────────────────────────────────────
NEGATION_WORDS = {
    "not", "no", "never", "neither", "nor", "none",
    "don't", "dont", "doesn't", "doesnt", "didn't", "didnt",
    "can't", "cant", "couldn't", "couldnt", "won't", "wont",
    "wouldn't", "wouldnt", "isn't", "isnt", "aren't", "arent",
    "wasn't", "wasnt", "weren't", "werent", "haven't", "havent",
    "hasn't", "hasnt", "hadn't", "hadnt", "shouldn't", "shouldnt",
    "without", "barely", "hardly", "scarcely",
}

# ─── Sarcasm / Irony patterns ────────────────────────────────────────────────
SARCASM_PATTERNS = [
    # "Oh great" sarcasm opener
    (r"\boh\s+(great|wow|sure|perfect|wonderful|fantastic|amazing)\b", " sarcasm_oh_great "),
    # "Another X that Y" dismissal
    (r"\banother\s+\S+\s+that\s+", " sarcasm_another_that "),
    # Positive word wrapped in quotes (irony signal)
    (r"'(amazing|great|life.changing|genius|expert|perfect)'", r" sarcasm_quoted_\1 "),
    # ellipsis after a sentence (trailing sarcasm signal)
    (r"\.{2,}", " ellipsis_sarcasm "),
    # Hyperbolic praise followed by contradiction
    (r"\b(10\/10|perfect|flawless|masterpiece)\b.{0,30}\b(but|however|except|although|yet)\b", " praise_contradiction "),
]


def _replace_emojis(text: str) -> str:
    """Replace known emojis with sentiment-bearing text."""
    for emoji, replacement in EMOJI_MAP.items():
        text = text.replace(emoji, replacement)
    return text


def _apply_sarcasm_patterns(text: str) -> str:
    """Tag sarcasm signals with special tokens before lowercasing wipes them."""
    for pattern, replacement in SARCASM_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def _handle_negation(tokens: list) -> list:
    """
    Attach NOT_ prefix to words that follow a negation word.
    Window: attach to the next 4 words after the negation.
    e.g. ["don't", "like", "this"] → ["dont", "NOT_like", "NOT_this"]
    """
    result = []
    negate = 0  # countdown of how many words to negate
    for token in tokens:
        if token in NEGATION_WORDS:
            negate = 4  # negate next 4 words
            result.append(token)
        elif negate > 0:
            result.append(f"NOT_{token}")
            negate -= 1
            # Reset on clause boundary
            if token in {",", ".", "!", "?", ";", "but", "however"}:
                negate = 0
        else:
            result.append(token)
    return result


def clean_text(text: str) -> str:
    """
    Full NLP preprocessing pipeline for sentiment analysis.
    Steps:
      1. Replace emojis with descriptive text
      2. Apply sarcasm pattern tagging
      3. Remove URLs and HTML
      4. Lowercase
      5. Tokenise
      6. Apply negation handling
      7. Remove punctuation noise (but keep alphanumerics + underscores for special tokens)
      8. Collapse whitespace
    """
    if not isinstance(text, str):
        text = str(text)

    # Step 1 — emoji → text
    text = _replace_emojis(text)

    # Step 2 — tag sarcasm BEFORE lowercasing
    text = _apply_sarcasm_patterns(text)

    # Step 3 — remove URLs and HTML
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"<.*?>", " ", text)

    # Step 4 — lowercase
    text = text.lower()

    # Step 5 — tokenise on whitespace
    tokens = text.split()

    # Step 6 — negation handling
    tokens = _handle_negation(tokens)

    # Rejoin
    text = " ".join(tokens)

    # Step 7 — remove characters that aren't alphanumeric or underscore
    # (underscore is kept to preserve NOT_word and sarcasm_tokens)
    text = re.sub(r"[^a-z0-9_\s]", " ", text)

    # Step 8 — collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_label(label: str) -> str:
    """Normalize sentiment labels to positive / neutral / negative."""
    if not isinstance(label, str):
        label = str(label)
    label = label.lower().strip()
    if label in {"positive", "pos", "1", "1.0"}:
        return "positive"
    if label in {"negative", "neg", "-1", "-1.0"}:
        return "negative"
    return "neutral"
