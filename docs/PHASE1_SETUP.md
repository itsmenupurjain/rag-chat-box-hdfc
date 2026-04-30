# Phase 1: Project Setup & Data Corpus Definition

## Overview
Phase 1 establishes the foundation for the Mutual Fund FAQ Assistant by setting up the project structure, defining the data corpus, and configuring all necessary files.

**Status:** ✅ Complete  
**Implementation Date:** April 25, 2026

---

## Objectives

1. ✅ Create organized project directory structure
2. ✅ Define and configure 5 HDFC mutual fund schemes from Groww
3. ✅ Set up configuration files with all URLs
4. ✅ Implement logging system
5. ✅ Create setup validation script
6. ✅ Configure environment variables

---

## Implementation Details

### 1. Project Structure Created

```
rag chat box/
├── data/
│   ├── raw/              # Downloaded HTML files from Groww
│   ├── processed/        # Extracted and cleaned text
│   └── vectors/          # FAISS/Chroma vector indexes
├── src/                  # Source code
│   ├── logger.py         # Logging utility
│   └── phase1_setup.py   # Setup validation
├── tests/                # Unit tests
├── configs/              # Configuration files
│   ├── groww_urls.json   # Groww mutual fund URLs
│   └── schemes.json      # Scheme details
├── logs/                 # Application logs
├── docs/                 # Documentation
├── .env                  # Environment variables
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
└── README.md
```

### 2. Configuration Files

#### groww_urls.json
**Location:** `configs/groww_urls.json`

**Contents:**
- AMC: HDFC Mutual Fund
- Platform: Groww
- 5 scheme URLs from Groww
- 3 additional reference sources (AMFI, SEBI, HDFC AMC)

#### schemes.json
**Location:** `configs/schemes.json`

**Contents:**
- Detailed metadata for each scheme
- Category, plan type, risk level
- Benchmark index information

### 3. Selected Schemes

| # | Scheme Name | Category | Plan Type | Risk Level |
|---|-------------|----------|-----------|------------|
| 1 | HDFC Mid-Cap Fund | Mid Cap | Direct-Growth | Very High |
| 2 | HDFC Equity Fund | Large Cap | Direct-Growth | Very High |
| 3 | HDFC Focused Fund | Focused Fund | Direct-Growth | Very High |
| 4 | HDFC ELSS Tax Saver Fund | ELSS | Direct-Plan-Growth | Very High |
| 5 | HDFC Large Cap Fund | Large Cap | Direct-Growth | Very High |

### 4. URLs Configured

**Primary Sources (Groww - 5 URLs):**
```
1. https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth
2. https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth
3. https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth
4. https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth
5. https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth
```

**Reference Sources (3 URLs):**
```
- AMFI: https://www.amfiindia.com/investor-awareness
- SEBI: https://www.sebi.gov.in/investor.html
- HDFC AMC: https://www.hdfcfund.com/
```

### 5. Dependencies

**File:** `requirements.txt`

```txt
streamlit>=1.28.0
groq>=0.4.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.4
beautifulsoup4>=4.12.0
lxml>=4.9.0
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
```

### 6. Environment Configuration

**File:** `.env`

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Note:** Users must replace with their actual Groq API key from https://console.groq.com

---

## Code Implementation

### logger.py
**Location:** `src/logger.py`

**Purpose:** Centralized logging utility

**Features:**
- Console and file handlers
- Configurable log levels
- Automatic log directory creation
- Formatted timestamp output

**Usage:**
```python
from logger import setup_logger
logger = setup_logger("phase1_setup", "phase1_setup.log")
```

### phase1_setup.py
**Location:** `src/phase1_setup.py`

**Purpose:** Validate project setup and configurations

**Functions:**
1. `validate_project_structure()` - Check all directories exist
2. `load_configurations()` - Load JSON config files
3. `verify_urls_accessibility()` - Test if URLs are reachable
4. `display_corpus_summary()` - Show data corpus overview
5. `main()` - Orchestrate all setup steps

---

## How to Run

### Step 1: Install Dependencies
```bash
cd "c:\Users\Admin\Desktop\rag chat box"
pip install -r requirements.txt
```

### Step 2: Configure API Key
Edit `.env` file and add your Groq API key:
```env
GROQ_API_KEY=gsk_your_actual_key
```

### Step 3: Execute Phase 1 Setup
```bash
cd src
python phase1_setup.py
```

### Expected Output
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

---

## Key Design Decisions

### 1. HTML-Only Data Source
- **Decision:** Use only web pages, no PDFs
- **Rationale:** Easier to parse, always up-to-date, simpler maintenance
- **Impact:** Removed PDF libraries (PyPDF2, pdfplumber)

### 2. Groww as Primary Platform
- **Decision:** Use Groww URLs as main data source
- **Rationale:** Clean UI, structured data, comprehensive information
- **Impact:** Need to handle potential JavaScript rendering

### 3. Configuration-Driven Approach
- **Decision:** Store URLs and scheme details in JSON files
- **Rationale:** Easy to modify without code changes, version control friendly
- **Impact:** Can add/remove schemes by editing config files

### 4. Modular Logging System
- **Decision:** Create reusable logger utility
- **Rationale:** Consistent logging across all phases, easy debugging
- **Impact:** Each phase gets its own log file

---

## Validation Results

### Project Structure
- ✅ All 8 required directories created
- ✅ No missing dependencies

### Configuration Files
- ✅ groww_urls.json: Valid JSON, 5 schemes + 3 references
- ✅ schemes.json: Valid JSON, complete metadata

### URL Accessibility
- Test each URL with HTTP GET request
- Log success/failure status
- Continue even if some URLs fail (handled in Phase 2)

---

## Files Created

| File | Type | Purpose |
|------|------|---------|
| `configs/groww_urls.json` | Config | URL definitions |
| `configs/schemes.json` | Config | Scheme metadata |
| `src/logger.py` | Code | Logging utility |
| `src/phase1_setup.py` | Code | Setup validation |
| `requirements.txt` | Config | Dependencies |
| `.env` | Config | Environment vars |
| `.gitignore` | Config | Git rules |
| `PHASE1_README.md` | Docs | Phase 1 guide |

---

## Testing

### Manual Testing
```bash
# Test configuration loading
python -c "import json; print(json.load(open('configs/groww_urls.json'))['amc'])"

# Test logger
python -c "from src.logger import setup_logger; logger = setup_logger('test'); logger.info('Test')"

# Test URL accessibility
python -c "import requests; print(requests.get('https://groww.in').status_code)"
```

### Automated Testing
Run the setup script:
```bash
python src/phase1_setup.py
```

---

## Known Limitations

1. **URL Blocking:** Some websites may block automated requests
   - **Mitigation:** Add user-agent headers, use delays in Phase 2

2. **JavaScript Content:** Groww may use dynamic content loading
   - **Mitigation:** Use Playwright/Selenium if BeautifulSoup fails

3. **Rate Limiting:** Too many requests may trigger blocks
   - **Mitigation:** Cache downloaded HTML locally

---

## Next Steps

**Phase 2: Data Ingestion & HTML Parsing**
- Scrape HTML from all configured URLs
- Parse and extract relevant mutual fund data
- Clean and structure the extracted content
- Save raw HTML to `data/raw/`
- Save processed data to `data/processed/`

---

## Success Criteria

- ✅ Project structure created and validated
- ✅ Configuration files properly formatted
- ✅ All URLs accessible (or gracefully handled)
- ✅ Logging system functional
- ✅ Setup script runs without errors
- ✅ Clear documentation provided

---

## References

- **Architecture Document:** `docs/ARCHITECTURE.md`
- **Problem Statement:** `problem statement.md`
- **Groq API:** https://console.groq.com
- **Groww:** https://groww.in/mutual-funds

---

**Phase 1 Status:** ✅ Complete  
**Next Phase:** Phase 2 - Data Ingestion & HTML Parsing
