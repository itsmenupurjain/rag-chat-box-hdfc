# Phase 1: Project Setup & Data Corpus Definition

## ✅ Status: Complete

Phase 1 establishes the foundation for the Mutual Fund FAQ Assistant.

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Edit `.env` file and add your Groq API key:
```env
GROQ_API_KEY=your_actual_api_key_here
```

Get your key from: https://console.groq.com

### 3. Run Setup
```bash
cd src
python phase1_setup.py
```

---

## What's Included

### Configuration Files
- `configs/groww_urls.json` - 5 Groww URLs + reference sources
- `configs/schemes.json` - Scheme metadata

### Source Code
- `src/logger.py` - Logging utility
- `src/phase1_setup.py` - Setup validation script

### Data
- 5 HDFC Mutual Fund schemes from Groww
- HTML web pages only (NO PDFs)

---

## Selected Schemes

| # | Scheme | Category |
|---|--------|----------|
| 1 | HDFC Mid-Cap Fund | Mid Cap |
| 2 | HDFC Equity Fund | Large Cap |
| 3 | HDFC Focused Fund | Focused Fund |
| 4 | HDFC ELSS Tax Saver Fund | ELSS |
| 5 | HDFC Large Cap Fund | Large Cap |

---

## URLs

**Primary Sources:**
1. https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth
2. https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth
3. https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth
4. https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth
5. https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth

---

## Next Phase

➡️ **Phase 2: Data Ingestion & HTML Parsing**

---

For detailed documentation, see: `docs/PHASE1_SETUP.md`
