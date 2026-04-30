from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
from src.logger import setup_logger

logger = setup_logger("html_parser", "ingestion.log")

class GrowwParser:
    def __init__(self):
        pass

    def parse(self, html_content, url):
        soup = BeautifulSoup(html_content, 'lxml')
        
        next_data_script = soup.find('script', id='__NEXT_DATA__')
        
        if next_data_script:
            try:
                json_data = json.loads(next_data_script.string)
                page_props = json_data.get('props', {}).get('pageProps', {})
                mf_data = page_props.get('mfServerSideData', {})
                
                if mf_data:
                    # Risk is often in return_stats or meta_desc
                    risk = mf_data.get('risk')
                    if not risk and mf_data.get('return_stats'):
                        risk = mf_data.get('return_stats')[0].get('risk')
                    
                    # Map fields from mfServerSideData
                    data = {
                        "scheme_name": mf_data.get('scheme_name'),
                        "url": url,
                        "scrape_date": datetime.now().strftime("%Y-%m-%d"),
                        "data": {
                            "nav": f"₹{mf_data.get('nav')}" if mf_data.get('nav') else None,
                            "nav_date": mf_data.get('nav_date'),
                            "min_sip": f"₹{mf_data.get('min_sip_investment')}" if mf_data.get('min_sip_investment') else None,
                            "min_lumpsum": f"₹{mf_data.get('min_investment_amount')}" if mf_data.get('min_investment_amount') else None,
                            "aum": f"₹{mf_data.get('aum'):,.2f} Cr" if mf_data.get('aum') else None,
                            "expense_ratio": f"{mf_data.get('expense_ratio')}%" if mf_data.get('expense_ratio') else None,
                            "riskometer": risk,
                            "fund_manager": mf_data.get('fund_manager'),
                            "benchmark": mf_data.get('benchmark_name') or mf_data.get('benchmark'),
                            "inception_date": mf_data.get('launch_date'),
                            "exit_load": mf_data.get('exit_load'),
                            "category": mf_data.get('category'),
                            "sub_category": mf_data.get('sub_category'),
                            "crisil_rating": mf_data.get('crisil_rating'),
                            "groww_rating": mf_data.get('groww_rating'),
                            "pros": [a.get('analysis_desc') for a in mf_data.get('analysis', []) if a.get('analysis_type') == 'PROS'],
                            "cons": [a.get('analysis_desc') for a in mf_data.get('analysis', []) if a.get('analysis_type') == 'CONS']
                        }
                    }
                    return data
            except Exception as e:
                logger.warning(f"Failed to parse JSON from __NEXT_DATA__: {e}")

        logger.info("Using HTML fallback for parsing")
        return self._parse_html_fallback(soup, url)

    def _parse_html_fallback(self, soup, url):
        data = {
            "scheme_name": self._extract_text_by_selector(soup, "h1"),
            "url": url,
            "scrape_date": datetime.now().strftime("%Y-%m-%d"),
            "data": {}
        }
        data["data"]["nav"] = self._extract_value_after_label(soup, "NAV")
        data["data"]["min_sip"] = self._extract_value_after_label(soup, "Min. for SIP")
        data["data"]["aum"] = self._extract_value_after_label(soup, "Fund size (AUM)")
        data["data"]["expense_ratio"] = self._extract_value_after_label(soup, "Expense ratio")
        
        risk_pill = soup.find("div", class_="pill12Pill", string=re.compile(r"Risk", re.I))
        if risk_pill:
            data["data"]["riskometer"] = risk_pill.get_text(strip=True)
            
        return data

    def _extract_text_by_selector(self, soup, selector):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else None

    def _extract_value_after_label(self, soup, label):
        label_tag = soup.find(string=re.compile(rf"{label}", re.I))
        if not label_tag:
            return None
        parent = label_tag.find_parent()
        if not parent:
            return None
        container = parent.find_parent()
        if container:
            value_tag = container.find(class_=re.compile(r"bodyXLargeHeavy|bodyBaseHeavy|contentPrimary"))
            if value_tag and value_tag != parent:
                return value_tag.get_text(strip=True)
        return None
