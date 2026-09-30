from transformers import pipeline

MODEL_ID = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
clf = pipeline("sentiment-analysis", model=MODEL_ID)

long_para = " ".join(
    ["The semester had its ups and downs, with long nights in the library and"
     " short breaks between classes that never felt long enough."] * 30
)

cases = [
    ("happy positive", "The new library timings made exam week so much easier."),
    ("happy negative", "My laptop froze twice during the online quiz."),
    ("sarcasm", "Oh wonderful, the Wi-Fi died right before submission."),
    ("negation", "I wouldn't say it was bad."),
    ("neutral", "The bus arrived at 9."),
    ("emojis only", "🔥🔥🔥"),
    ("empty string", ""),
    (f"long paragraph (~{len(long_para.split())} words)", long_para),
    # extra positive candidates (the library sentence came out NEGATIVE)
    ("positive 2", "Our group presentation went smoother than any rehearsal we did."),
    ("positive 3", "The cafeteria finally added a vegetarian biryani and it tastes amazing."),
    # extra candidates for a fooling case
    ("sarcasm 2", "Great, another group project where I do all the work."),
    ("double negation", "The food was not bad at all."),
    ("mixed", "The movie was not good, but the soundtrack was not terrible either."),
    ("praise via complaint", "I can't stop listening to this album, it's ruining my sleep."),
]

for name, text in cases:
    preview = text if len(text) <= 70 else text[:67] + "..."
    try:
        r = clf(text, truncation=True)[0]
        print(f"[{name}] {preview!r} -> {r['label']} ({r['score']:.4f})")
    except Exception as e:
        print(f"[{name}] {preview!r} -> ERROR: {type(e).__name__}: {e}")
