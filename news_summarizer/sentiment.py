# sentiment.py
import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_sentiment_model():
    return pipeline(
        "sentiment-analysis",
        model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
    )

def analyze_sentiment(text: str) -> dict:
    if not text.strip():
        return {"label": "Neutral", "score": 1.0}

    try:
        classifier = load_sentiment_model()
        result = classifier(text[:1000])[0]
        label = result["label"].capitalize()
        score = round(float(result["score"]), 4)
        return {"label": label, "score": score}
    except Exception as e:
        return {"label": "Error", "score": 0.0, "error": str(e)}
