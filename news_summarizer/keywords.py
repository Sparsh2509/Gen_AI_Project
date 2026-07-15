# keywords.py
import streamlit as st
from keybert import KeyBERT

@st.cache_resource
def load_keybert_model():
    return KeyBERT()

def extract_keywords(text: str, top_n: int = 10) -> list:
    if not text.strip():
        return []

    try:
        kw_model = load_keybert_model()
        keywords = kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 1),
            stop_words="english",
            top_n=top_n
        )
        return keywords
    except Exception as e:
        return [("Error", 0.0)]
