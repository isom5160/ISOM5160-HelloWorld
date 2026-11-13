import streamlit as st
from transformers import pipeline

# 1. Page Configuration
st.set_page_config(page_title="Sentiment Analysis App", page_icon="💬")

st.title("💬 Sentiment Analysis App")
st.write(
    "This app estimates the **tone** (sentiment) of your text, not its factual accuracy."
)


# 2. Load the Model (Cached so it doesn't reload on every interaction)
@st.cache_resource
def load_pipeline():
  # Note: Meta-Llama-3-8B-Instruct is a large, gated generative model.
  # Ensure you have a GPU/sufficient RAM and are logged in via `huggingface-cli login`.
  return pipeline(
      "sentiment-analysis", model="meta-llama/Meta-Llama-3-8B-Instruct"
  )


with st.spinner("Loading model... This may take a moment."):
  sentiment_pipeline = load_pipeline()

# 3. User Input
default_text = (
    "Deep Learning (DL) represents a highly promising approach to developing\n"
    "applications in Artificial Intelligence (AI)."
)

text = st.text_area("Enter text to analyze:", value=default_text, height=150)

# 4. Run Analysis on Button Click
if st.button("Analyze Sentiment", type="primary"):
  if text.strip():
    with st.spinner("Analyzing..."):
      result = sentiment_pipeline(text)
      label = result[0]["label"]
      score = result[0]["score"]

    # 5. Display Results
    st.subheader("Results")
    col1, col2 = st.columns(2)
    col1.metric("Sentiment", label)
    col2.metric("Confidence Score", f"{score:.4f}")
  else:
    st.warning("Please enter some text before analyzing.")
