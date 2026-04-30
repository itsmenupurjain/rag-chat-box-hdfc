# Phase 2: Data Ingestion & HTML Parsing

## Overview
Phase 2 focuses on scraping HTML content from Groww URLs and extracting relevant mutual fund information.

**Status:** 🚧 In Progress  
**Implementation Date:** TBD

---

## Objectives

1. Scrape HTML from 5 Groww mutual fund URLs
2. Parse HTML to extract fund details
3. Clean and structure the data
4. Save raw HTML to `data/raw/`
5. Save processed data to `data/processed/`

---

## Implementation Plan

### 1. Data Ingestion Script
**File:** `src/data_ingestion.py`

**Functions:**
- `fetch_html(url)` - Download HTML from URL
- `parse_html(html_content)` - Extract relevant sections
- `extract_fund_data(parsed_html)` - Get fund details
- `save_raw_html(html, filename)` - Save raw HTML
- `save_processed_data(data, filename)` - Save processed JSON

### 2. HTML Parser
**File:** `src/html_parser.py`

**Technologies:**
- BeautifulSoup4 for HTML parsing
- lxml for faster parsing
- Regular expressions for pattern matching

**Data to Extract:**
- Scheme name
- Expense ratio
- Exit load
- Minimum SIP amount
- Minimum lumpsum amount
- Riskometer
- Fund manager
- Benchmark
- AUM (Assets Under Management)
- Inception date
- NAV (Net Asset Value)

### 3. Data Structure

**Output Format (JSON):**
```json
{
  "scheme_name": "HDFC Mid-Cap Fund",
  "url": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
  "scrape_date": "2026-04-25",
  "data": {
    "expense_ratio": "0.55%",
    "exit_load": "1% if redeemed within 1 year",
    "min_sip": "₹500",
    "min_lumpsum": "₹5,000",
    "riskometer": "Very High",
    "fund_manager": "Name",
    "benchmark": "NIFTY Midcap 150 TRI",
    "aum": "₹50,000 Cr",
    "nav": "₹150.25"
  }
}
```

---

## How to Run

```bash
cd src
python data_ingestion.py
```

---

## Expected Output

- 5 HTML files in `data/raw/`
- 5 JSON files in `data/processed/`
- Log file in `logs/ingestion.log`

---

## Challenges & Solutions

### Challenge 1: JavaScript-Rendered Content
**Problem:** Data loaded dynamically via JavaScript  
**Solution:** Use Playwright or Selenium if needed

### Challenge 2: Anti-Scraping Measures
**Problem:** Groww may block automated requests  
**Solution:** Add delays, use proper headers, respect robots.txt

### Challenge 3: Inconsistent HTML Structure
**Problem:** Different pages may have different layouts  
**Solution:** Flexible parsing with fallback strategies

---

## Files to Create

- `src/data_ingestion.py`
- `src/html_parser.py`
- `tests/test_html_parsing.py`

---

## Success Criteria

- ✅ All 5 URLs successfully scraped
- ✅ HTML files saved locally
- ✅ Data extracted and structured
- ✅ No missing critical fields
- ✅ Error handling for failed requests

---

**Phase 2 Status:** 🚧 Not Started  
**Previous Phase:** Phase 1 - Project Setup ✅  
**Next Phase:** Phase 3 - Vector Database & Embeddings
