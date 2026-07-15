# app.py
import re
import os
import streamlit as st
from dotenv import load_dotenv

from summarizer import generate_summary
from sentiment import analyze_sentiment
from keywords import extract_keywords
from entities import extract_entities
from qa import answer_question

load_dotenv()

st.set_page_config(
    page_title="News Summarization & Sentiment Analysis",
    page_icon="📰",
    layout="centered"
)

st.title("📰 Intelligent News Summarization and Sentiment Analysis System")
st.markdown("Paste a news article below and click **Analyze** to extract insights using AI and NLP.")

# Load API key
env_key = os.getenv("GROQ_API_KEY", "")
if env_key == "your_groq_api_key_here":
    env_key = ""

if env_key:
    api_key = env_key
else:
    api_key = st.text_input(
        "🔑 Enter your Groq API Key:",
        type="password",
        help="Get your free key at https://console.groq.com/keys"
    )

st.markdown("---")

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = re.findall(r'\b\w+\b', text)
    return ' '.join(tokens)

# Session State Initialization
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "article" not in st.session_state:
    st.session_state.article = ""
if "cleaned" not in st.session_state:
    st.session_state.cleaned = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "sentiment" not in st.session_state:
    st.session_state.sentiment = {}
if "keywords" not in st.session_state:
    st.session_state.keywords = []
if "entities" not in st.session_state:
    st.session_state.entities = {}
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

# Section 1: News Article Input
st.header("1. News Article Input")

article_input = st.text_area(
    "Paste your news article here:",
    height=220,
    placeholder="Copy and paste any news article here (at least 2-3 paragraphs)..."
)

col1, col2 = st.columns([2, 1])
with col1:
    analyze_btn = st.button("🔍 Analyze Article", type="primary", use_container_width=True)
with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.analyzed = False
        st.session_state.article = ""
        st.session_state.cleaned = ""
        st.session_state.summary = ""
        st.session_state.sentiment = {}
        st.session_state.keywords = []
        st.session_state.entities = {}
        st.session_state.qa_history = []
        st.rerun()

# Run Analysis Pipeline
if analyze_btn:
    if not article_input.strip():
        st.warning("⚠️ Please paste a news article before clicking Analyze.")
    elif not api_key:
        st.error("❌ Please enter your Groq API Key above.")
    else:
        with st.spinner("Running NLP pipeline..."):
            st.session_state.article = article_input
            st.session_state.cleaned = preprocess(article_input)
            st.session_state.sentiment = analyze_sentiment(article_input)
            st.session_state.keywords = extract_keywords(article_input)
            st.session_state.entities = extract_entities(article_input)
            st.session_state.summary = generate_summary(st.session_state.cleaned, api_key)
            st.session_state.analyzed = True
        st.success("✅ Analysis complete!")

# Display Results
if st.session_state.analyzed:
    with st.expander("🔧 NLP Preprocessing Details"):
        token_count = len(st.session_state.cleaned.split())
        st.write(f"**Total tokens after cleaning:** {token_count}")
        st.write("**Steps applied:** Lowercase → Remove extra spaces → Tokenize")
        st.caption("Cleaned text preview (first 300 chars):")
        st.code(st.session_state.cleaned[:300])

    st.markdown("---")

    # Section 2: Summary
    st.header("2. Summary")
    st.markdown(st.session_state.summary)

    st.markdown("---")

    # Section 3: Sentiment
    st.header("3. Sentiment Analysis")
    sent = st.session_state.sentiment
    label = sent.get("label", "Unknown")
    score = sent.get("score", 0.0)

    if label == "Positive":
        st.success(f"😊 **{label}** — Confidence: {score:.1%}")
    elif label == "Negative":
        st.error(f"😠 **{label}** — Confidence: {score:.1%}")
    else:
        st.info(f"😐 **{label}** — Confidence: {score:.1%}")

    st.markdown("---")

    # Section 4: Keywords
    st.header("4. Top 10 Keywords (KeyBERT)")
    kws = st.session_state.keywords
    if kws:
        for i, (word, score_val) in enumerate(kws, 1):
            st.write(f"**{i}.** `{word}` — Score: {score_val:.4f}")
    else:
        st.write("No keywords extracted.")

    st.markdown("---")

    # Section 5: Named Entities
    st.header("5. Named Entities (spaCy)")
    ents = st.session_state.entities
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("👤 Persons")
        if ents.get("Person"):
            for p in ents["Person"]:
                st.write(f"• {p}")
        else:
            st.caption("None found.")

        st.subheader("🏢 Organizations")
        if ents.get("Organization"):
            for o in ents["Organization"]:
                st.write(f"• {o}")
        else:
            st.caption("None found.")

    with col_b:
        st.subheader("📍 Locations")
        if ents.get("Location"):
            for l in ents["Location"]:
                st.write(f"• {l}")
        else:
            st.caption("None found.")

        st.subheader("📅 Dates")
        if ents.get("Date"):
            for d in ents["Date"]:
                st.write(f"• {d}")
        else:
            st.caption("None found.")

    st.markdown("---")

    # Section 6: Ask Questions
    st.header("6. Ask Questions About the Article")
    st.write("Ask anything about the article. The AI will only use the article content to answer.")
    st.caption(f"📝 *Active article size in memory: {len(st.session_state.article)} characters*")

    question = st.text_input(
        "Your question:",
        placeholder="e.g. Who is mentioned in this article? What happened?"
    )

    if st.button("💬 Get Answer"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Finding answer..."):
                ans = answer_question(st.session_state.article, question, api_key)
            st.session_state.qa_history.append({"q": question, "a": ans})

    # Show Q&A history
    if st.session_state.qa_history:
        st.subheader("Q&A History")
        for item in reversed(st.session_state.qa_history):
            st.markdown(f"**Q:** {item['q']}")
            st.markdown(f"**A:** {item['a']}")
            st.markdown("---")

# Show instructions only when not analyzed and button is not clicked
if not st.session_state.analyzed and not analyze_btn:
    st.info("👆 Paste a news article above and click Analyze Article to begin.")
