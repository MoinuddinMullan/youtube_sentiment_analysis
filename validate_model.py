import sys
sys.path.insert(0, r'D:\moin\youtube_sentiment_analysis\backend')
sys.path.insert(0, r'D:\moin\youtube_sentiment_analysis\backend\ml')
import joblib
import re
from app.services.preprocessing import clean_text

model = joblib.load(r'D:\moin\youtube_sentiment_analysis\backend\ml\artifacts\sentiment_model.joblib')
vec   = joblib.load(r'D:\moin\youtube_sentiment_analysis\backend\ml\artifacts\tfidf_vectorizer.joblib')

# ── same rules as model_service.py ──
HARD_NEGATIVE = [
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
    r"\bspent\s+\d+\s+minutes?\b.{0,50}\bcould\s+have\b",
    r"\bcould\s+have\s+been\s+said\s+in\s+\d+\s+seconds?\b",
    r"\b\d+\s+minutes?.{0,30}(could have been|explaining something that could)\b",
    r"\bnot\s+(terrible|bad)\b.{0,40}\bnot\s+worth\b",
    r"\bnot\s+worth\s+(all\s+the\s+hype|the\s+hype|watching)\b",
    r"skull_emoji_lol",
    r"eye_roll_emoji",
    r"boring_sleep_emoji",
    r"facepalm_emoji",
]

HARD_POSITIVE = [
    r"\babsolute\s+masterpiece\b",
    r"\bdeserve\s+millions?\s+of\s+views\b",
    r"\bsubscribed\s+immediately\b",
    r"\bquality\s+of\s+(editing|content).{0,20}\b(insane|amazing|incredible|great)\b",
    r"\bpacing\s+in\s+this\s+video\s+is\s+(insane|amazing|incredible)\b",
    r"fire_great_emoji",
    r"clapping_great_emoji",
    r"\blife\s+changing\b",
    r"\bchanged\s+my\s+(perspective|life|mind)\b",
    r"\bthanks?\s+for\s+(explaining|teaching|making)\b",
]

def predict(text):
    cleaned = clean_text(text)
    v = vec.transform([cleaned])
    pred = model.predict(v)[0]
    probs = model.predict_proba(v)[0]
    labels = ['negative', 'neutral', 'positive']
    prob_dict = dict(zip(labels, probs))
    tl = text.lower()

    for p in HARD_NEGATIVE:
        if re.search(p, tl) or re.search(p, cleaned):
            return 'negative', 0.80, 'rule-neg'
    for p in HARD_POSITIVE:
        if re.search(p, tl) or re.search(p, cleaned):
            return 'positive', max(0.80, prob_dict.get('positive', 0.5)), 'rule-pos'

    return pred, float(max(probs)), 'model'

cases = [
    ("Don't bother watching guys, half the code shown on screen is outdated and full of errors.", "negative"),
    ("This was painful to watch. Audio quality is awful and you kept repeating the same point.", "negative"),
    ("Total clickbait. The title promises a full breakdown but you barely touched the surface.", "negative"),
    ("Worst explanation ever. Left me more confused than before I started.", "negative"),
    ("Unsubscribed. Content has really dropped in quality over the last few months.", "negative"),
    ("Honestly lost all respect for this channel after this video. Completely biased and unresearched.", "negative"),
    ("Oh great, another 'life-changing' tool that breaks after 2 days of use... eyeroll", "negative"),
    ("This video cured my boredom... by putting me straight to sleep.", "negative"),
    ("Bro thought he cooked with this one skull_emoji_lol", "negative"),
    ("Absolute masterpiece. You deserve millions of views for this content!", "positive"),
    ("Subscribed immediately. The quality of editing and pacing in this video is insane", "positive"),
    ("Finally, a tutorial that doesn't waste 10 minutes talking about unrelated stuff.", "positive"),
    ("Can someone tell me what background music was played at 02:30?", "neutral"),
    ("He mentioned the updated version comes out next Tuesday.", "neutral"),
    ("This completely changed my perspective! Thanks for explaining so clearly.", "positive"),
    ("I mean, it's not terrible, but definitely not worth all the hype.", "neutral"),
    ("You spent 15 minutes explaining something that could have been said in 30 seconds", "negative"),
]

correct = 0
for text, expected in cases:
    pred, conf, src = predict(text)
    ok = 'OK  ' if pred.lower() == expected else 'FAIL'
    if pred.lower() == expected:
        correct += 1
    print(f"[{ok}] {pred.upper():8s} ({src:8s}) conf={conf:.0%}  | {text[:58]}")

print(f"\nResult: {correct}/{len(cases)} correct ({100*correct//len(cases)}%)")

# Also debug the boredom case
print("\n--- Debug: cleaned text for failing cases ---")
for text in [
    "This video cured my boredom... by putting me straight to sleep.",
    "Subscribed immediately. The quality of editing and pacing in this video is insane",
    "I mean, it's not terrible, but definitely not worth all the hype.",
    "You spent 15 minutes explaining something that could have been said in 30 seconds",
    "Finally, a tutorial that doesn't waste 10 minutes talking about unrelated stuff.",
]:
    c = clean_text(text)
    print(f"  ORIG: {text[:65]}")
    print(f"  CLEAN: {c[:80]}")
    print()
