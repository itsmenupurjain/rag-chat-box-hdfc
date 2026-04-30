import schedule
import time
import os
import subprocess
from src.logger import setup_logger

logger = setup_logger("scheduler", "ingestion.log")

def run_pipeline():
    """
    Runs the full ingestion and indexing pipeline.
    """
    logger.info("CRON: Starting scheduled data refresh...")
    
    try:
        # 1. Run Data Ingestion
        logger.info("CRON: Phase 2 - Ingesting data...")
        subprocess.run(["python", "-m", "src.data_ingestion"], check=True)
        
        # 2. Run Indexing
        logger.info("CRON: Phase 3 - Indexing data...")
        subprocess.run(["python", "-m", "src.index_data"], check=True)
        
        logger.info("CRON: Scheduled data refresh complete!")
    except Exception as e:
        logger.error(f"CRON: Pipeline failed: {e}")

def start_scheduler():
    # Schedule the refresh at 09:30 AM every day
    # Note: Ensure the system time is set to IST or adjust accordingly
    schedule.every().day.at("09:30").do(run_pipeline)
    
    logger.info("Scheduler started. Waiting for 09:30 AM...")
    
    while True:
        schedule.run_pending()
        time.sleep(60) # Check every minute

if __name__ == "__main__":
    start_scheduler()
