"""
Simplified Configuration for Ethiopian Banking Apps Analysis - TASK 1
No automatic directory creation or validation on import
"""

import os
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

# =============================================================================
# BASIC CONFIGURATION - NO AUTOMATIC EXECUTION
# =============================================================================

APP_IDS = {
    'CBE': os.getenv('CBE_APP_ID', 'com.combanketh.mobilebanking'),
    'BOA': os.getenv('BOA_APP_ID', 'com.boa.boaMobileBanking'),
    'DASHEN': os.getenv('DASHEN_APP_ID', 'com.cr2.amolelight')
}

BANK_NAMES = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia', 
    'DASHEN': 'Dashen Bank'
}

SCRAPING_CONFIG = {
    'reviews_per_bank': int(os.getenv('REVIEWS_PER_BANK', 450)),
    'max_retries': int(os.getenv('MAX_RETRIES', 3)),
    'retry_delay': int(os.getenv('RETRY_DELAY', 5)),
    'lang': os.getenv('SCRAPER_LANG', 'en'),
    'country': os.getenv('SCRAPER_COUNTRY', 'et')
}

DATA_PATHS = {
    'raw': 'data/raw',
    'processed': 'data/processed',
    'raw_reviews': 'data/raw/reviews_raw.csv',
    'processed_reviews': 'data/processed/reviews_cleaned.csv',
    'app_info': 'data/raw/app_info.csv'
}

# =============================================================================
# HELPER FUNCTIONS - BUT DON'T CALL THEM AUTOMATICALLY
# =============================================================================

def create_data_directories():
    """Create directories - call this manually from your scraper"""
    os.makedirs(DATA_PATHS['raw'], exist_ok=True)
    os.makedirs(DATA_PATHS['processed'], exist_ok=True)
    print(" Data directories created")

def get_config_summary():
    """Get config summary - call this manually if needed"""
    return {
        'total_banks': len(APP_IDS),
        'reviews_per_bank': SCRAPING_CONFIG['reviews_per_bank'],
        'language': SCRAPING_CONFIG['lang']
    }

