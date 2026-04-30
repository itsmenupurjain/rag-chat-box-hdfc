# Mutual Fund FAQ Assistant - Documentation Index

## Project Overview
A facts-only RAG-based FAQ assistant for mutual fund schemes using Groww as the reference platform.

**AMC:** HDFC Mutual Fund  
**Platform:** Groww  
**Architecture:** RAG (Retrieval-Augmented Generation)  
**LLM:** Groq (Llama 3.3 70B)

---

## Documentation Structure

Each phase has its own detailed documentation file:

| Phase | Document | Status | Description |
|-------|----------|--------|-------------|
| **Architecture** | [ARCHITECTURE.md](ARCHITECTURE.md) | ✅ Complete | Overall system architecture |
| **Phase 1** | [PHASE1_SETUP.md](PHASE1_SETUP.md) | ✅ Complete | Project setup & data corpus |
| **Phase 2** | [PHASE2_INGESTION.md](PHASE2_INGESTION.md) | 🚧 In Progress | Data ingestion & HTML parsing |
| **Phase 3** | [PHASE3_EMBEDDINGS.md](PHASE3_EMBEDDINGS.md) | 📋 Planned | Vector database & embeddings |
| **Phase 4** | [PHASE4_RETRIEVAL.md](PHASE4_RETRIEVAL.md) | 📋 Planned | Retrieval engine |
| **Phase 5** | [PHASE5_LLM.md](PHASE5_LLM.md) | 📋 Planned | LLM generation & validation |
| **Phase 6** | [PHASE6_REFUSAL.md](PHASE6_REFUSAL.md) | 📋 Planned | Refusal handler |
| **Phase 7** | [PHASE7_UI.md](PHASE7_UI.md) | 📋 Planned | Streamlit UI |

---

## Quick Navigation

### 📋 Planning & Architecture
- [ARCHITECTURE.md](ARCHITECTURE.md) - Complete system design
- [../problem statement.md](../problem%20statement.md) - Project requirements

### 🔧 Implementation Phases

#### Phase 1: Project Setup ✅
- [PHASE1_SETUP.md](PHASE1_SETUP.md) - Setup documentation
- [../PHASE1_README.md](../PHASE1_README.md) - Quick start guide

#### Phase 2: Data Ingestion 🚧
- [PHASE2_INGESTION.md](PHASE2_INGESTION.md) - HTML scraping plan

#### Phase 3: Embeddings 📋
- [PHASE3_EMBEDDINGS.md](PHASE3_EMBEDDINGS.md) - Vector database plan

#### Phase 4: Retrieval 📋
- [PHASE4_RETRIEVAL.md](PHASE4_RETRIEVAL.md) - Search engine plan

#### Phase 5: LLM Generation 📋
- [PHASE5_LLM.md](PHASE5_LLM.md) - Response generation plan

#### Phase 6: Refusal Handler 📋
- [PHASE6_REFUSAL.md](PHASE6_REFUSAL.md) - Advisory query handling

#### Phase 7: UI 📋
- [PHASE7_UI.md](PHASE7_UI.md) - Streamlit interface plan

---

## Project Structure

```
rag chat box/
│
├── docs/                           # 📚 Documentation
│   ├── INDEX.md                    # This file
│   ├── ARCHITECTURE.md             # System architecture
│   ├── PHASE1_SETUP.md             # Phase 1 docs
│   ├── PHASE2_INGESTION.md         # Phase 2 docs
│   ├── PHASE3_EMBEDDINGS.md        # Phase 3 docs
│   ├── PHASE4_RETRIEVAL.md         # Phase 4 docs
│   ├── PHASE5_LLM.md               # Phase 5 docs
│   ├── PHASE6_REFUSAL.md           # Phase 6 docs
│   └── PHASE7_UI.md                # Phase 7 docs
│
├── data/                           # 💾 Data storage
│   ├── raw/                        # Downloaded HTML
│   ├── processed/                  # Cleaned data
│   └── vectors/                    # Vector indexes
│
├── src/                            # 🔨 Source code
│   ├── logger.py                   # Logging utility
│   ├── phase1_setup.py             # Setup script
│   ├── data_ingestion.py           # HTML scraper (Phase 2)
│   ├── html_parser.py              # HTML parser (Phase 2)
│   ├── document_processor.py       # Chunking (Phase 3)
│   ├── embedding_engine.py         # Embeddings (Phase 3)
│   ├── vector_store.py             # Vector DB (Phase 3)
│   ├── retrieval_engine.py         # Search (Phase 4)
│   ├── llm_generator.py            # LLM (Phase 5)
│   ├── response_validator.py       # Validation (Phase 5)
│   ├── refusal_handler.py          # Refusals (Phase 6)
│   └── app.py                      # UI (Phase 7)
│
├── configs/                        # ⚙️ Configuration
│   ├── groww_urls.json             # URL definitions
│   └── schemes.json                # Scheme metadata
│
├── tests/                          # 🧪 Unit tests
│
├── logs/                           # 📝 Application logs
│
├── .env                            # 🔑 Environment variables
├── .gitignore                      # Git rules
├── requirements.txt                # Dependencies
├── PHASE1_README.md                # Phase 1 quick start
└── problem statement.md            # Project requirements
```

---

## Implementation Status

### ✅ Completed
- Phase 1: Project Setup & Data Corpus Definition
  - Project structure created
  - Configuration files defined
  - URLs validated
  - Logging system implemented

### 🚧 In Progress
- Phase 2: Data Ingestion & HTML Parsing
  - HTML scraper implementation
  - Data extraction logic

### 📋 Planned
- Phase 3: Vector Database & Embeddings
- Phase 4: Retrieval Engine
- Phase 5: LLM Generation & Validation
- Phase 6: Refusal Handler
- Phase 7: Streamlit UI
- Testing & Integration

---

## Key Features

### Facts-Only Responses
- ✅ Maximum 3 sentences per response
- ✅ Exactly 1 citation link
- ✅ Last updated date footer
- ✅ No investment advice

### Multi-Thread Chat
- ✅ Independent conversation threads
- ✅ Session state management
- ✅ Chat history preservation

### Advisory Query Refusal
- ✅ Pattern-based detection
- ✅ Polite refusal messages
- ✅ Educational resource links

### Data Sources
- ✅ 5 HDFC schemes from Groww
- ✅ AMFI, SEBI reference sources
- ✅ HTML web pages only (no PDFs)

---

## Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Edit `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run Phase 1 Setup
```bash
cd src
python phase1_setup.py
```

### 4. Follow Phase Documentation
Each phase has detailed instructions in its respective document.

---

## Configuration Files

### groww_urls.json
Contains all URLs to scrape:
- 5 Groww mutual fund pages
- 3 reference sources (AMFI, SEBI, HDFC AMC)

### schemes.json
Scheme metadata:
- Category, plan type, risk level
- Benchmark information

### .env
Environment variables:
- GROQ_API_KEY for LLM access

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | >=1.28.0 | Web UI framework |
| groq | >=0.4.0 | LLM API client |
| sentence-transformers | >=2.2.0 | Text embeddings |
| faiss-cpu | >=1.7.4 | Vector similarity search |
| beautifulsoup4 | >=4.12.0 | HTML parsing |
| lxml | >=4.9.0 | Fast HTML parser |
| requests | >=2.31.0 | HTTP requests |
| pandas | >=2.0.0 | Data manipulation |
| numpy | >=1.24.0 | Numerical operations |
| python-dotenv | >=1.0.0 | Environment variables |

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

## API Reference

### Groq API
- **Endpoint:** `POST https://api.groq.com/openai/v1/chat/completions`
- **Model:** `llama-3.3-70b-versatile`
- **Documentation:** https://console.groq.com/docs

### Get API Key
1. Visit https://console.groq.com
2. Sign up for free account
3. Generate API key
4. Add to `.env` file

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Factual Accuracy | > 95% |
| Response Time | < 3 seconds |
| Citation Inclusion | 100% |
| Advisory Query Refusal | 100% |
| Response Length | ≤ 3 sentences |
| User Satisfaction | > 4/5 rating |

---

## Troubleshooting

### Common Issues

**Issue:** Module not found  
**Solution:** `pip install -r requirements.txt`

**Issue:** GROQ_API_KEY not set  
**Solution:** Update `.env` file with your API key

**Issue:** URLs not accessible  
**Solution:** Check internet connection, some sites may block scraping

**Issue:** No results from search  
**Solution:** Ensure Phase 2 and 3 completed successfully

---

## Next Steps

1. **Complete Phase 2:** Implement HTML scraper
2. **Test Data Ingestion:** Verify all 5 URLs scraped
3. **Implement Phase 3:** Create vector embeddings
4. **Build Retrieval:** Set up similarity search
5. **Integrate LLM:** Connect Groq API
6. **Add Refusals:** Implement advisory detection
7. **Build UI:** Create Streamlit interface
8. **Test End-to-End:** Full system testing

---

## References

- **Problem Statement:** `../problem statement.md`
- **Architecture:** `ARCHITECTURE.md`
- **Groww Platform:** https://groww.in/mutual-funds
- **AMFI:** https://www.amfiindia.com
- **SEBI:** https://www.sebi.gov.in
- **HDFC AMC:** https://www.hdfcfund.com

---

## Contact & Support

For issues or questions:
1. Check phase-specific documentation
2. Review log files in `logs/` directory
3. Consult architecture document
4. Refer to problem statement

---

**Last Updated:** April 25, 2026  
**Project Status:** Phase 1 Complete ✅  
**Next Phase:** Phase 2 - Data Ingestion 🚧
