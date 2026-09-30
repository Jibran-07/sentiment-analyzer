import pandas as pd
import streamlit as st
from transformers import pipeline

MODEL_ID = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
LOW_CONFIDENCE = 0.75
EXAMPLES = [
    "The cafeteria finally added a vegetarian biryani and it tastes amazing.",
    "The lab printer jammed again ten minutes before the deadline.",
    "Our group presentation went smoother than any rehearsal we did.",
    "The new parking policy is confusing and nobody explained it to us.",
]

st.set_page_config(page_title="Sentiment Analyzer", page_icon="💬")


@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model=MODEL_ID)


if "history" not in st.session_state:
    st.session_state.history = []
if "text" not in st.session_state:
    st.session_state.text = ""
if "example_idx" not in st.session_state:
    st.session_state.example_idx = 0

# Sidebar: example filler
with st.sidebar:
    st.header("Try an example")
    st.caption("Fills the text box with a sample sentence.")
    if st.button("Load example sentence"):
        st.session_state.text = EXAMPLES[st.session_state.example_idx % len(EXAMPLES)]
        st.session_state.example_idx += 1

# Header
st.title("💬 Sentiment Analyzer")
st.markdown(
    "**Muhammad Jibran Narejo** (B04-0923-000020) · "
    "**Sheikh Muhammad Abdullah** (B04-0923-000044)  \n"
    "BSCS Sec A · CS4106 Foundations of Generative AI"
)

text = st.text_area("Enter some text to analyze:", key="text", height=140)

if st.button("Analyze", type="primary"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            with st.spinner("Analyzing..."):
                result = load_model()(text, truncation=True)[0]
            label = result["label"]
            score = result["score"]
            pct = f"{score * 100:.2f}%"
            if label == "POSITIVE":
                st.success(f"POSITIVE 😊 (confidence {pct})")
            else:
                st.error(f"NEGATIVE 😞 (confidence {pct})")
            st.progress(score)
            if score < LOW_CONFIDENCE:
                st.info("Low confidence: the model is unsure about this one, so treat the label with caution.")
            snippet = text if len(text) <= 60 else text[:57] + "..."
            st.session_state.history.insert(0, {"Text": snippet, "Label": label, "Confidence": pct})
            st.session_state.history = st.session_state.history[:5]
        except Exception as e:
            st.error(f"Something went wrong while analyzing: {e}")

if st.session_state.history:
    st.subheader("Session history (last 5)")
    st.table(pd.DataFrame(st.session_state.history))

st.divider()
st.caption(
    "Model limits: binary only (POSITIVE/NEGATIVE, no neutral class) · "
    "often misses sarcasm and irony · input truncated to 512 tokens · "
    f"model: {MODEL_ID}"
)
