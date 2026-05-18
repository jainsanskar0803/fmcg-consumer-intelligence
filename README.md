# FMCG Consumer Intelligence Platform

> AI-powered FMCG consumer analytics platform using RAG, LLMs, LangChain, ChromaDB, Streamlit, and MongoDB.

An enterprise-style consumer intelligence dashboard that helps FMCG companies analyze customer reviews, track competitor sentiment, identify product issues, and generate executive-level business insights using Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs).

Built as a full-stack GenAI portfolio project demonstrating practical implementation of modern AI systems.

---

# Features

## Sentiment Analytics Dashboard
- Real-time KPI tracking
- Sentiment distribution analysis
- Consumer trend visualization
- Keyword and issue detection

## Competitor Intelligence
- Brand-vs-brand comparison
- Radar charts and heatmaps
- Market sentiment benchmarking
- Product performance insights

## AI-Powered Q&A
- Ask natural language questions about reviews
- Context-aware AI responses using RAG
- Semantic search with ChromaDB
- Intelligent review retrieval

## Executive Summary Generator
- AI-generated strategic business reports
- Downloadable summaries
- Product and competitor insights
- Executive-ready recommendations

## Review Upload System
- Upload custom CSV/TXT datasets
- Built-in demo review datasets
- Automatic preprocessing pipeline

## Hinglish Support
- Handles mixed Hindi-English customer reviews
- Improved sentiment understanding for Indian FMCG market

## MongoDB Logging
- Stores uploaded datasets
- Tracks AI queries
- Analytics interaction logging

---

# Tech Stack

## Frontend
- Streamlit
- Plotly
- Custom CSS UI

## Backend & AI
- Python
- LangChain
- Gemini API
- Groq API
- ChromaDB
- Sentence Transformers

## Database
- MongoDB

## AI Capabilities
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Sentiment Analysis
- LLM-Powered Insights

---

# Project Structure

```bash
fmcg_intelligence/
│
├── app.py
├── frontend/
├── backend/
├── data/
├── vectorstore/
├── utils/
├── assets/
├── requirements.txt
├── .env.example
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/jainsanskar0803/fmcg-consumer-intelligence.git
cd fmcg-consumer-intelligence
```

## 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
GROQ_API_KEY=your_api_key
MONGODB_URI=your_mongodb_uri
```

## 5. Run Application

```bash
streamlit run app.py
```

---

# Use Cases

- FMCG consumer sentiment analysis
- Competitor benchmarking
- Product issue identification
- AI-powered business intelligence
- Executive reporting automation
- Customer review analytics

---

# Highlights

- Enterprise-style analytics dashboard
- Real-world RAG implementation
- Production-inspired UI/UX
- Modern GenAI architecture
- Portfolio-ready deployment project
- Practical AI business use case

---

# Future Improvements

- Multi-language sentiment analysis
- Real-time social media ingestion
- Advanced forecasting models
- Voice-based analytics assistant
- Automated competitor alerts

---

# License

MIT License

---

# Author

Sanskar Jain

GitHub: https://github.com/jainsanskar0803
