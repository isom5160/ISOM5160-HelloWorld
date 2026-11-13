# ISOM5160 Practice - Security Alert Triage Streamlit app
# Model answer. A simple top-to-bottom script (no functions).
# The NLP model is a public Hugging Face text-classification
# model trained to flag phishing-like email text.

import streamlit as st
from transformers import pipeline

st.title("ISOM5160-newwwww2")
st.write("Security Alert Triage")
st.write(
    "Paste a short email or security alert. "
    "The model will classify it as phishing-like or legitimate."
)

# Use a Hugging Face fine-grained token from Streamlit Cloud secrets
# if one is set. Do not put the token in this file.
hf_token = None
if "HF_TOKEN" in st.secrets:
    hf_token = st.secrets["HF_TOKEN"]

alert_text = st.text_area(
    "Email or security alert",
    value=(
        "Urgent: verify your payroll password at "
        "http://secure-payrol1-update.example now or account locked."
    ),
    height=140,
)

if st.button("Classify alert"):
    if alert_text.strip():
        # Removed device="cpu" and model_kwargs to maximize compatibility on CPU-only Streamlit Cloud
        classifier = pipeline(
            "text-classification",
            model="ealvaradob/bert-finetuned-phishing",
            token=hf_token,
        )
        
        result = classifier(alert_text)[0]
        raw_label = result["label"]
        score = result["score"]
        
        display_label = raw_label
        if raw_label == "phishing":
            display_label = "phishing-like"
        elif raw_label == "benign":
            display_label = "legitimate"
            
        st.subheader("Model result")
        st.write("Label: " + display_label)
        st.write("Confidence: " + str(round(score, 3)))
        st.caption(
            "This is a teaching demo. A security analyst should review "
            "the result before acting on it."
        )
    else:
        st.write("Please paste an email or security alert first.")
