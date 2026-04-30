# Mutual Fund FAQ Assistant

A facts-only RAG-based FAQ assistant for mutual fund schemes using Groww as the reference platform.

---

## Project Overview

**AMC:** HDFC Mutual Fund  
**Platform:** Groww  
**Architecture:** RAG (Retrieval-Augmented Generation)  
**LLM:** Groq (Llama 3.3 70B)  
**Status:** Phase 1 Complete ✅

---

## Phase-Wise Structure

Each phase is organized in its own folder with source code, configs, and documentation:

```
rag chat box/
│
├── phase 1/              ✅ COMPLETE - Project Setup
│   ├── src/              Source code
│   ├── configs/          Configuration files
│   ├── data/             Data storage
│   ├── logs/             Log files
│   ├── requirements.txt  Dependencies
│   ├── .env              Environment variables
│   └── README.md         Phase 1 guide
│
├── phase 2/              🚧 IN PROGRESS - Data Ingestion
│   ├── src/              (To be implemented)
│   ├── data/             HTML files
│   └── README.md
│
├── phase 3/              📋 PLANNED - Vector Embeddings
│   └── README.md
│
├── phase 4/              📋 PLANNED - Retrieval Engine
│   └── README.md
│
├── phase 5/              📋 PLANNED - LLM Generation
│   └── README.md
│
├── phase 6/              📋 PLANNED - Refusal Handler
│   └── README.md
│
├── phase 7/              📋 PLANNED - Streamlit UI
│   └── README.md
│
├── docs/                 📚 Documentation
│   ├── INDEX.md          Master documentation index
│   ├── ARCHITECTURE.md   System architecture
│   ├── PHASE1_SETUP.md   Phase 1 detailed docs
│   ├── PHASE2_INGESTION.md
│   ├── PHASE3_EMBEDDINGS.md
│   ├── PHASE4_RETRIEVAL.md
│   ├── PHASE5_LLM.md
│   ├── PHASE6_REFUSAL.md
│   └── PHASE7_UI.md
│
├── problem statement.md  Project requirements
└── requirements.txt      Global dependencies
```

---

## Quick Start

### Phase 1: Setup (Current)

```bash
# Navigate to Phase 1
cd "phase 1"

# Install dependencies
pip install -r requirements.txt

# Configure API key
# Edit .env file and add your Groq API key

# Run setup
cd src
python phase1_setup.py
```

---

## Selected Schemes

| # | Scheme | Category | Plan |
|---|--------|----------|------|
| 1 | HDFC Mid-Cap Fund | Mid Cap | Direct-Growth |
| 2 | HDFC Equity Fund | Large Cap | Direct-Growth |
| 3 | HDFC Focused Fund | Focused Fund | Direct-Growth |
| 4 | HDFC ELSS Tax Saver Fund | ELSS | Direct-Plan-Growth |
| 5 | HDFC Large Cap Fund | Large Cap | Direct-Growth |

---

## Key Features

- ✅ Facts-only responses (no investment advice)
- ✅ Maximum 3 sentences per response
- ✅ Exactly 1 citation link
- ✅ Last updated date footer
- ✅ Multi-thread chat support
- ✅ Advisory query refusal
- ✅ HTML web pages only (no PDFs)

---

## Documentation

- **Master Index:** [docs/INDEX.md](docs/INDEX.md)
- **Architecture:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Phase 1:** [phase 1/README.md](phase%201/README.md)

---

## Dependencies

- streamlit >= 1.28.0
- groq >= 0.4.0
- sentence-transformers >= 2.2.0
- faiss-cpu >= 1.7.4
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0
- requests >= 2.31.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- python-dotenv >= 1.0.0

---

## API Requirements

### Groq API
- **Get Key:** https://console.groq.com
- **Model:** llama-3.3-70b-versatile
- **Free Tier:** 30 requests/minute

---

## Progress

- ✅ Phase 1: Project Setup & Data Corpus
- 🚧 Phase 2: Data Ingestion & HTML Parsing
- 📋 Phase 3: Vector Database & Embeddings
- 📋 Phase 4: Retrieval Engine
- 📋 Phase 5: LLM Generation & Validation
- 📋 Phase 6: Refusal Handler
- 📋 Phase 7: Streamlit UI

---

## Next Steps

1. ✅ Complete Phase 1 setup
2. 🚧 Implement Phase 2 data ingestion
3. 📋 Continue through Phase 7

---

**Last Updated:** April 25, 2026  
**Project Status:** Phase 1 Complete ✅
