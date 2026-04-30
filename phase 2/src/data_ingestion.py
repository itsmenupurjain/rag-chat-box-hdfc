"""
Phase 2: Data Ingestion & HTML Parsing
Scrapes HTML content from Groww URLs and extracts mutual fund data
"""

import os
import sys
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logger import setup_logger

logger = setup_logger("phase2_ingestion", "phase2_ingestion.log")


class DataIngestion:
    """Handles web scraping and HTML parsing for mutual fund data"""
    
    def __init__(self, config_path=None):
        """Initialize with configuration"""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "configs",
                "groww_urls.json"
            )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.data_dir = os.path.dirname(os.path.dirname(__file__))
        self.raw_dir = os.path.join(self.data_dir, "data", "raw")
        self.processed_dir = os.path.join(self.data_dir, "data", "processed")
        
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        
        logger.info("DataIngestion initialized")
        logger.info(f"Raw data directory: {self.raw_dir}")
        logger.info(f"Processed data directory: {self.processed_dir}")
    
    def fetch_html(self, url, timeout=10):
        """Fetch HTML content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            logger.info(f"Successfully fetched: {url[:60]}...")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {str(e)}")
            return None
    
    def save_raw_html(self, scheme_name, html_content):
        """Save raw HTML to file"""
        filename = f"{scheme_name.replace(' ', '_')}.html"
        filepath = os.path.join(self.raw_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Saved raw HTML: {filepath}")
        return filepath
    
    def parse_scheme_page(self, html_content, scheme_info):
        """Parse HTML and extract mutual fund information"""
        soup = BeautifulSoup(html_content, 'lxml')
        
        extracted_data = {
            'scheme_name': scheme_info.get('name', ''),
            'category': scheme_info.get('category', ''),
            'plan': scheme_info.get('plan', ''),
            'risk_level': scheme_info.get('risk_level', ''),
            'source_url': scheme_info.get('url', ''),
            'scraped_at': datetime.now().isoformat(),
            'fund_size': None,
            'expense_ratio': None,
            'exit_load': None,
            'min_sip': None,
            'min_lumpsum': None,
            'nav': None,
            'returns_1y': None,
            'returns_3y': None,
            'returns_5y': None,
            'description': None,
            'key_features': [],
            'top_holdings': [],
            'asset_allocation': '{}'  # Changed to string for parquet compatibility
        }
        
        # Extract text content
        text_content = soup.get_text(separator=' ', strip=True)
        
        # Try to extract NAV
        nav_text = soup.find(string=lambda text: text and 'NAV' in text)
        if nav_text:
            parent = nav_text.parent if hasattr(nav_text, 'parent') else None
            if parent:
                extracted_data['nav'] = parent.get_text(strip=True)
        
        # Extract description (first large paragraph)
        paragraphs = soup.find_all('p')
        if paragraphs:
            for p in paragraphs:
                text = p.get_text(strip=True)
                if len(text) > 100:  # Likely a description
                    extracted_data['description'] = text[:500]
                    break
        
        # Extract fund metrics from typical patterns
        patterns = {
            'fund_size': ['Fund Size', 'AUM'],
            'expense_ratio': ['Expense Ratio'],
            'exit_load': ['Exit Load'],
            'min_sip': ['Minimum SIP'],
            'min_lumpsum': ['Minimum Lumpsum']
        }
        
        all_text = soup.get_text()
        for key, keywords in patterns.items():
            for keyword in keywords:
                if keyword.lower() in all_text.lower():
                    # Find the value near the keyword
                    idx = all_text.lower().find(keyword.lower())
                    if idx != -1:
                        snippet = all_text[idx:idx+100]
                        extracted_data[key] = snippet[:50]
                        break
        
        # Extract key features (look for lists or bullet points)
        lists = soup.find_all(['ul', 'ol'])
        for ul in lists[:3]:  # First 3 lists
            items = ul.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                if text and len(text) > 10:
                    extracted_data['key_features'].append(text)
        
        # Store full text for later processing
        extracted_data['full_text'] = text_content[:5000]  # First 5000 chars
        
        logger.info(f"Parsed scheme: {extracted_data['scheme_name']}")
        return extracted_data
    
    def ingest_all_schemes(self):
        """Main method to ingest all schemes"""
        logger.info("=" * 70)
        logger.info("PHASE 2: Starting Data Ingestion")
        logger.info("=" * 70)
        
        schemes = self.config.get('schemes', [])
        additional_sources = self.config.get('additional_sources', [])
        
        all_data = []
        successful = 0
        failed = 0
        
        # Process primary schemes
        for scheme in schemes:
            logger.info(f"\nProcessing: {scheme['name']}")
            
            # Fetch HTML
            html_content = self.fetch_html(scheme['url'])
            if not html_content:
                failed += 1
                continue
            
            # Save raw HTML
            self.save_raw_html(scheme['name'], html_content)
            
            # Parse and extract data
            parsed_data = self.parse_scheme_page(html_content, scheme)
            all_data.append(parsed_data)
            successful += 1
        
        # Process additional sources
        for source in additional_sources:
            logger.info(f"\nProcessing reference: {source['name']}")
            html_content = self.fetch_html(source['url'])
            if html_content:
                self.save_raw_html(source['name'], html_content)
                successful += 1
            else:
                failed += 1
        
        # Save processed data
        if all_data:
            df = pd.DataFrame(all_data)
            output_path = os.path.join(self.processed_dir, 'schemes_data.parquet')
            df.to_parquet(output_path, index=False)
            logger.info(f"\nSaved processed data to: {output_path}")
        
        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 2 INGESTION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Total schemes: {len(schemes)}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Data saved to: {self.processed_dir}")
        
        return successful, failed


def main():
    """Run Phase 2 ingestion"""
    ingestion = DataIngestion()
    successful, failed = ingestion.ingest_all_schemes()
    
    if successful > 0:
        logger.info("\n✅ Phase 2 completed successfully!")
        logger.info(f"   - {successful} sources processed")
        logger.info(f"   - Check data/raw/ for HTML files")
        logger.info(f"   - Check data/processed/ for parquet file")
    else:
        logger.error("\n❌ Phase 2 failed - no data ingested")
        sys.exit(1)


if __name__ == "__main__":
    main()
