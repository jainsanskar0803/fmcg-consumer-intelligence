# AI FMCG Consumer Intelligence System

A realistic internal analytics platform for FMCG companies to understand customer sentiment, track complaints, and compare against competitors — using AI.

Built for Emami Ltd. as a demo project. Works instantly with built-in datasets, no setup needed beyond an API key.

---

## What it does

- Shows customer sentiment across Emami and competitor brands
- Lets you ask plain-English questions about review data and get AI answers
- Generates executive-level reports in one click
- Handles Hinglish reviews (mixed Hindi-English)
- Stores upload history and Q&A logs in MongoDB

---

## Setup (5 minutes)

### 1. Clone and install

```bash
git clone https://github.com/yourusername/fmcg-intelligence.git
cd fmcg-intelligence
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add your API key

```bash
cp .env.example .env
```

Open `.env` and add your OpenAI key:

```
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
```

Get a free key at https://platform.openai.com/api-keys

### 3. Run

```bash
streamlit run app.py
```

App opens at http://localhost:8501

---

## MongoDB setup (optional)

MongoDB is used to log file uploads and Q&A history. The app works fine without it.

**To enable locally:**
```bash
# Mac
brew install mongodb-community
brew services start mongodb-community

# Linux
sudo apt install mongodb
sudo systemctl start mongodb
```

**For cloud deployment (Streamlit Cloud):**
1. Create a free cluster at https://cloud.mongodb.com
2. Copy the connection string
3. Add it to `.env`: `MONGO_URI=mongodb+srv://...`

The app shows "MongoDB — Offline (optional)" in the sidebar if it's not running. Everything else still works.

---

## Project structure

```
fmcg_intelligence/
├── app.py                    ← run this
├── pages/
│   ├── dashboard.py          ← main analytics dashboard
│   ├── competitor.py         ← brand comparison page
│   ├── ask_questions.py      ← AI Q&A interface
│   ├── executive_summary.py  ← report generator
│   └── upload.py             ← file upload + demo datasets
├── components/
│   ├── styles.py             ← all CSS styling
│   ├── sidebar.py            ← navigation sidebar
│   └── charts.py             ← Plotly chart builders
├── services/
│   ├── data_loader.py        ← reads CSV / TXT files
│   ├── llm_service.py        ← OpenAI / Gemini integration
│   └── mongodb_service.py    ← upload history & query logs
├── rag/
│   └── embeddings.py         ← ChromaDB vector search
├── utils/
│   ├── config.py             ← environment variables
│   └── helpers.py            ← data processing functions
├── data/
│   └── reviews_dataset.csv   ← 141 built-in reviews
├── .streamlit/config.toml    ← theme settings
├── .env.example              ← copy this to .env
└── requirements.txt
```

---

## Deploying to Streamlit Cloud

1. Push to GitHub (make sure `.env` is in `.gitignore`)
2. Go to https://share.streamlit.io → New app
3. Select your repo, set main file to `app.py`
4. Add secrets under Settings → Secrets:
   ```
   OPENAI_API_KEY = "sk-..."
   LLM_PROVIDER = "openai"
   MONGO_URI = "mongodb+srv://..."   # optional
   ```

---

## Tech stack

| Layer | What's used |
|---|---|
| UI | Streamlit |
| AI / LLM | OpenAI GPT-3.5 (or Gemini) |
| Vector search | ChromaDB + sentence-transformers |
| Orchestration | LangChain |
| Database | MongoDB |
| Charts | Plotly |
| Language | Python 3.10+ |

---

## Author

Created by **Sanskar**  
AI FMCG Consumer Intelligence System
