# Intelligent News Summarization and Sentiment Analysis System

A Gen AI project designed to analyze news articles using NLP (Natural Language Processing) and Large Language Models (LLMs). The application summarizes text, detects sentiment, extracts keywords, identifies named entities, and answers context-specific questions.

---

## 🔗 Live Demo / Deployment Link

The application is deployed and live at:
👉 **[genaiproject-usfs6sn83qvodjlkswkqmw.streamlit.app](https://genaiproject-usfs6sn83qvodjlkswkqmw.streamlit.app/)**

---

## 📁 Project Structure

```text
Gen_AI_Project/
├── app.py           → Main Streamlit dashboard (UI, preprocessing & pipeline)
├── summarizer.py    → Bullet-point news summarization (LangChain + Groq Llama-3.3)
├── sentiment.py     → Sentiment analysis pipeline (Hugging Face DistilBERT)
├── keywords.py      → Keyphrase & keyword extraction (KeyBERT)
├── entities.py      → Named Entity Recognition (spaCy NER)
├── qa.py            → Context-restricted Question Answering (LangChain + Groq)
├── requirements.txt → Project dependencies
├── .env             → API credentials configuration
└── README.md        → Documentation & Viva guide
```

---

## 🛠️ Tech Stack

| Module | Technology / Library | Description |
|---|---|---|
| **Frontend UI** | Streamlit | Lightweight web application framework |
| **LLM Orchestration** | LangChain | Framework for structuring prompt templates and chains |
| **Inference Engine** | Groq API | Ultra-fast Llama-3.3 LLM execution engine |
| **LLM Model** | Llama-3.3-70b-Versatile | State-of-the-art open source reasoning model |
| **Sentiment Analysis** | Hugging Face Transformers | Local DistilBERT classifier (3 classes) |
| **Keyword Extraction** | KeyBERT | BERT-based document-phrase similarity extractor |
| **Named Entities (NER)**| spaCy (`en_core_web_sm`) | Industrial-strength NLP tokenizer and entity tagger |

---

## 🚀 Setup and Installation

### 1. Set Up Virtual Environment
Activate your terminal inside the root workspace directory and run:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install Project Dependencies
Run the installation command inside the root directory:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Add API Key Configuration
Get a free Groq API key from [Groq Console](https://console.groq.com/keys). Open the `.env` file and insert the key:
```env
GROQ_API_KEY=gsk_your_actual_key_here
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```

---
