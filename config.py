"""
Configuration for Ethiopian Banking Apps Analysis
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Play Store App IDs for Ethiopian Banks
APP_IDS = {
    'CBE': os.getenv('CBE_APP_ID', 'com.cbe.mobilebanking'),
    'BOA': os.getenv('BOA_APP_ID', 'com.bankofabyssinia.mobilebanking'),
    'DASHEN': os.getenv('DASHEN_APP_ID', 'com.dashenbank.scmobile')
}

# Bank Names Mapping
BANK_NAMES = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia', 
    'DASHEN': 'Dashen Bank'
}

# Scraping Configuration
SCRAPING_CONFIG = {
    'reviews_per_bank': 500,  # Target per bank
    'max_retries': 3,
    'lang': 'en',            # English reviews
    'country': 'et'          # Ethiopia
}

# File Paths
DATA_PATHS = {
    'raw': 'data/raw',
    'processed': 'data/processed',
    'raw_reviews': 'data/raw/reviews_raw.csv',
    'processed_reviews': 'data/processed/reviews_cleaned.csv'
}