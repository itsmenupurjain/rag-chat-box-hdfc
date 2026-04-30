"""
Phase 1: Project Setup & Data Corpus Definition

This script:
1. Validates project structure
2. Loads and validates configuration files
3. Verifies Groww URLs are accessible
4. Initializes logging
"""

import os
import sys
import json
import requests
from logger import setup_logger

# Setup logger
logger = setup_logger("phase1_setup", "phase1_setup.log")

def validate_project_structure():
    """Validate that all required directories exist"""
    logger.info("Validating project structure...")
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    required_dirs = [
        "data/raw",
        "data/processed",
        "data/vectors",
        "src",
        "tests",
        "configs",
        "logs",
        "docs"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        full_path = os.path.join(base_dir, dir_path)
        if not os.path.exists(full_path):
            missing_dirs.append(dir_path)
            os.makedirs(full_path, exist_ok=True)
            logger.info(f"Created missing directory: {dir_path}")
    
    if not missing_dirs:
        logger.info("✅ All required directories exist")
    else:
        logger.warning(f"⚠️ Created {len(missing_dirs)} missing directories")
    
    return True

def load_configurations():
    """Load and validate configuration files"""
    logger.info("Loading configuration files...")
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    configs_dir = os.path.join(base_dir, "configs")
    
    # Load Groww URLs config
    groww_urls_path = os.path.join(configs_dir, "groww_urls.json")
    if not os.path.exists(groww_urls_path):
        logger.error(f"❌ Configuration file not found: {groww_urls_path}")
        return None
    
    with open(groww_urls_path, 'r', encoding='utf-8') as f:
        groww_config = json.load(f)
    
    logger.info(f"✅ Loaded Groww URLs configuration")
    logger.info(f"   AMC: {groww_config['amc']}")
    logger.info(f"   Platform: {groww_config['platform']}")
    logger.info(f"   Number of schemes: {len(groww_config['schemes'])}")
    
    # Load schemes config
    schemes_path = os.path.join(configs_dir, "schemes.json")
    if not os.path.exists(schemes_path):
        logger.error(f"❌ Configuration file not found: {schemes_path}")
        return None
    
    with open(schemes_path, 'r', encoding='utf-8') as f:
        schemes_config = json.load(f)
    
    logger.info(f"✅ Loaded schemes configuration")
    logger.info(f"   Total schemes: {len(schemes_config['schemes'])}")
    
    return {
        "groww": groww_config,
        "schemes": schemes_config
    }

def verify_urls_accessibility(configs, timeout=10):
    """Verify that all Groww URLs are accessible"""
    logger.info("Verifying URL accessibility...")
    
    groww_config = configs["groww"]
    schemes = groww_config["schemes"]
    additional_sources = groww_config.get("additional_sources", [])
    
    all_urls = [scheme["url"] for scheme in schemes]
    all_urls.extend([source["url"] for source in additional_sources])
    
    accessible_count = 0
    failed_urls = []
    
    for url in all_urls:
        try:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            if response.status_code == 200:
                accessible_count += 1
                logger.info(f"✅ Accessible: {url[:60]}...")
            else:
                failed_urls.append((url, response.status_code))
                logger.warning(f"⚠️ Failed ({response.status_code}): {url[:60]}...")
        except requests.RequestException as e:
            failed_urls.append((url, str(e)))
            logger.error(f"❌ Error accessing {url[:60]}...: {str(e)}")
    
    logger.info(f"\nURL Verification Summary:")
    logger.info(f"   Total URLs: {len(all_urls)}")
    logger.info(f"   Accessible: {accessible_count}")
    logger.info(f"   Failed: {len(failed_urls)}")
    
    if failed_urls:
        logger.warning("\nFailed URLs:")
        for url, error in failed_urls:
            logger.warning(f"   - {url[:60]}... ({error})")
    
    return accessible_count == len(all_urls)

def display_corpus_summary(configs):
    """Display a summary of the data corpus"""
    logger.info("\n" + "="*60)
    logger.info("DATA CORPUS SUMMARY")
    logger.info("="*60)
    
    groww_config = configs["groww"]
    schemes_config = configs["schemes"]
    
    logger.info(f"\nAMC: {groww_config['amc']}")
    logger.info(f"Platform: {groww_config['platform']}")
    
    logger.info(f"\nSelected Schemes ({len(schemes_config['schemes'])}):")
    for i, scheme in enumerate(schemes_config['schemes'], 1):
        logger.info(f"  {i}. {scheme['scheme_name']}")
        logger.info(f"     Category: {scheme['category']}")
        logger.info(f"     Plan: {scheme['plan_type']}")
        logger.info(f"     Risk: {scheme['risk_level']}")
    
    logger.info(f"\nAdditional Sources:")
    for source in groww_config.get('additional_sources', []):
        logger.info(f"  - {source['name']} ({source['type']})")
    
    logger.info(f"\nData Types: HTML web pages only (NO PDFs)")
    logger.info(f"Total Primary URLs: {len(groww_config['schemes'])}")
    logger.info(f"Total Reference URLs: {len(groww_config.get('additional_sources', []))}")
    logger.info("="*60)

def main():
    """Main Phase 1 setup function"""
    logger.info("="*60)
    logger.info("PHASE 1: Project Setup & Data Corpus Definition")
    logger.info("="*60)
    
    # Step 1: Validate project structure
    logger.info("\n[Step 1/4] Validating project structure...")
    validate_project_structure()
    
    # Step 2: Load configurations
    logger.info("\n[Step 2/4] Loading configurations...")
    configs = load_configurations()
    if configs is None:
        logger.error("❌ Failed to load configurations. Exiting.")
        sys.exit(1)
    
    # Step 3: Verify URLs
    logger.info("\n[Step 3/4] Verifying URL accessibility...")
    urls_accessible = verify_urls_accessibility(configs)
    
    if not urls_accessible:
        logger.warning("⚠️ Some URLs are not accessible. Check your internet connection.")
        logger.warning("   You can still proceed, but data ingestion may fail for those URLs.")
    
    # Step 4: Display corpus summary
    logger.info("\n[Step 4/4] Displaying corpus summary...")
    display_corpus_summary(configs)
    
    # Final status
    logger.info("\n" + "="*60)
    logger.info("✅ PHASE 1 SETUP COMPLETE")
    logger.info("="*60)
    logger.info("\nNext Steps:")
    logger.info("  1. Update .env file with your GROQ_API_KEY")
    logger.info("  2. Run Phase 2: Data Ingestion (data_ingestion.py)")
    logger.info("  3. Install dependencies: pip install -r requirements.txt")
    logger.info("="*60)

if __name__ == "__main__":
    main()
