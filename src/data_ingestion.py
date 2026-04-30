import requests
import os
import json
import time
from datetime import datetime
from src.html_parser import GrowwParser
from src.logger import setup_logger

logger = setup_logger("data_ingestion", "ingestion.log")

URLS = [
    "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
]

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

def ensure_dirs():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        logger.info(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

def save_raw_html(html, filename):
    filepath = os.path.join(RAW_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    logger.info(f"Saved raw HTML to {filepath}")

def save_processed_data(data, filename):
    filepath = os.path.join(PROCESSED_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved processed data to {filepath}")

def run_ingestion():
    ensure_dirs()
    parser = GrowwParser()
    
    for url in URLS:
        filename_base = url.split('/')[-1]
        
        # 1. Fetch
        html = fetch_html(url)
        if not html:
            continue
            
        # 2. Save Raw
        save_raw_html(html, f"{filename_base}.html")
        
        # 3. Parse
        try:
            logger.info(f"Parsing data for: {filename_base}")
            processed_data = parser.parse(html, url)
            
            # 4. Save Processed
            save_processed_data(processed_data, f"{filename_base}.json")
        except Exception as e:
            logger.error(f"Error parsing {url}: {e}")
            
        # Be nice to the server
        time.sleep(2)

if __name__ == "__main__":
    logger.info("Starting Phase 2: Data Ingestion & Parsing")
    run_ingestion()
    logger.info("Phase 2 Implementation Complete")
