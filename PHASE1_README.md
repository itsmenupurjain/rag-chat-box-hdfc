# Phase 1: Project Setup & Data Corpus Definition

## Overview
Phase 1 focuses on setting up the project structure, defining the data corpus, and configuring the system for the Mutual Fund FAQ Assistant.

## What's Included

### 1. Project Structure
```
rag chat box/
├── data/
│   ├── raw/           # Downloaded HTML files from Groww
│   ├── processed/     # Extracted and cleaned text
│   └── vectors/       # FAISS/Chroma vector indexes
├── src/               # Source code
├── tests/             # Unit tests
├── configs/           # Configuration files
│   ├── groww_urls.json       # Groww mutual fund URLs
│   └── schemes.json          # Scheme details
├── logs/              # Application logs
├── docs/              # Documentation
├── .env               # Environment variables (GROQ_API_KEY)
├── .gitignore
├── requirements.txt
└── README.md
```

### 2. Configuration Files

#### groww_urls.json
Contains all URLs to be scraped:
- 5 HDFC Mutual Fund schemes from Groww
- 3 additional reference sources (AMFI, SEBI, HDFC AMC)

#### schemes.json
Detailed information about each scheme:
- Scheme name
- Category (Mid Cap, Large Cap, ELSS, etc.)
- Plan type (Direct-Growth)
- Risk level
- Benchmark index

### 3. Selected Schemes

| # | Scheme Name | Category | Plan Type |
|---|-------------|----------|-----------|
| 1 | HDFC Mid-Cap Fund | Mid Cap | Direct-Growth |
| 2 | HDFC Equity Fund | Large Cap | Direct-Growth |
| 3 | HDFC Focused Fund | Focused Fund | Direct-Growth |
| 4 | HDFC ELSS Tax Saver Fund | ELSS | Direct-Plan-Growth |
| 5 | HDFC Large Cap Fund | Large Cap | Direct-Growth |

### 4. URLs to Scrape

**Primary Sources (Groww):**
1. https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth
2. https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth
3. https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth
4. https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth
5. https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth

**Reference Sources:**
- AMFI: https://www.amfiindia.com/investor-awareness
- SEBI: https://www.sebi.gov.in/investor.html
- HDFC AMC: https://www.hdfcfund.com/

## Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key
1. Open `.env` file
2. Replace `your_groq_api_key_here` with your actual Groq API key
3. Get your key from: https://console.groq.com

### Step 3: Run Phase 1 Setup
```bash
cd src
python phase1_setup.py
```

This will:
- ✅ Validate project structure
- ✅ Load configuration files
- ✅ Verify URL accessibility
- ✅ Display corpus summary

## Expected Output

```
============================================================
PHASE 1: Project Setup & Data Corpus Definition
============================================================

[Step 1/4] Validating project structure...
✅ All required directories exist

[Step 2/4] Loading configurations...
✅ Loaded Groww URLs configuration
   AMC: HDFC Mutual Fund
   Platform: Groww
   Number of schemes: 5

[Step 3/4] Verifying URL accessibility...
✅ Accessible: https://groww.in/mutual-funds/hdfc-mid-cap-fund...

[Step 4/4] Displaying corpus summary...
DATA CORPUS SUMMARY
============================================================
AMC: HDFC Mutual Fund
Platform: Groww

Selected Schemes (5):
  1. HDFC Mid-Cap Fund
     Category: Mid Cap
     Plan: Direct-Growth
     Risk: Very High
  ...

============================================================
✅ PHASE 1 SETUP COMPLETE
============================================================
```

## Key Points

- ✅ **Data Source:** Groww website (HTML pages only)
- ✅ **No PDFs:** All data will be scraped from web pages
- ✅ **5 Schemes:** Diverse categories (Mid Cap, Large Cap, ELSS, etc.)
- ✅ **Official Sources:** AMFI, SEBI for verification
- ✅ **Facts-Only:** System will not provide investment advice

## Next Steps

After completing Phase 1:
1. **Phase 2:** Data Ingestion - Scrape HTML from Groww URLs
2. **Phase 3:** Document Processing - Parse and chunk the data
3. **Phase 4:** Vector Embeddings - Create vector representations
4. **Phase 5:** Retrieval Engine - Build similarity search
5. **Phase 6:** LLM Generation - Integrate Groq API
6. **Phase 7:** Streamlit UI - Build the chat interface

## Troubleshooting

### Issue: "Module not found"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "URLs not accessible"
**Solution:** 
- Check internet connection
- Some URLs may block automated requests
- You can still proceed; Phase 2 will handle retries

### Issue: "GROQ_API_KEY not set"
**Solution:** Update `.env` file with your API key

## Files Created in Phase 1

| File | Purpose |
|------|---------|
| `configs/groww_urls.json` | URL configurations |
| `configs/schemes.json` | Scheme details |
| `src/logger.py` | Logging utility |
| `src/phase1_setup.py` | Setup validation script |
| `requirements.txt` | Python dependencies |
| `.env` | Environment variables |
| `.gitignore` | Git ignore rules |

---

**Status:** ✅ Phase 1 Complete
**Next:** Phase 2 - Data Ingestion & HTML Parsing
