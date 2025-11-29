"""
Data Preprocessing for Ethiopian Bank Reviews
Task 1: Data Cleaning
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
from config import DATA_PATHS


class ReviewPreprocessor:
    def __init__(self):
        self.input_path = DATA_PATHS['raw_reviews']
        self.output_path = DATA_PATHS['processed_reviews']
        self.df = None
    
    def load_data(self):
        """Load raw reviews data"""
        try:
            self.df = pd.read_csv(self.input_path)
            print(f" Loaded {len(self.df)} raw reviews")
            return True
        except Exception as e:
            print(f" Failed to load data: {e}")
            return False
    
    def remove_duplicates(self):
        """Remove duplicate reviews"""
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=['review_text', 'user_name', 'review_date'])
        removed = before - len(self.df)
        print(f" Removed {removed} duplicate reviews")
    
    def handle_missing_data(self):
        """Handle missing values"""
        # Remove reviews with no text
        before = len(self.df)
        self.df = self.df.dropna(subset=['review_text'])
        self.df = self.df[self.df['review_text'].str.strip() != '']
        removed = before - len(self.df)
        print(f" Removed {removed} empty reviews")
        
        # Fill other missing values
        self.df['rating'] = self.df['rating'].fillna(0)
        self.df['user_name'] = self.df['user_name'].fillna('Anonymous')
    
    def normalize_dates(self):
        """Convert dates to YYYY-MM-DD format"""
        self.df['review_date'] = pd.to_datetime(self.df['review_date']).dt.strftime('%Y-%m-%d')
        print(" Dates normalized to YYYY-MM-DD")
    
    def clean_text(self):
        """Basic text cleaning"""
        self.df['review_text'] = self.df['review_text'].str.strip()
        self.df['review_text'] = self.df['review_text'].replace(r'\s+', ' ', regex=True)
        print(" Text cleaning completed")
    
    def select_final_columns(self):
        """Select only required columns"""
        final_columns = ['review_text', 'rating', 'review_date', 'bank_name', 'source']
        
        # Only keep columns that exist
        available_columns = [col for col in final_columns if col in self.df.columns]
        self.df = self.df[available_columns]
        
        # Rename to match requirements
        self.df = self.df.rename(columns={
            'review_text': 'review',
            'review_date': 'date',
            'bank_name': 'bank'
        })
        
        print(" Final columns selected")
    
    def save_clean_data(self):
        """Save processed data"""
        import os
        os.makedirs('data/processed', exist_ok=True)
        self.df.to_csv(self.output_path, index=False)
        print(f" Clean data saved to: {self.output_path}")
    
    def generate_report(self):
        """Generate preprocessing report"""
        print("\n📊 PREPROCESSING REPORT:")
        print("=" * 40)
        print(f"Final reviews: {len(self.df)}")
        print(f"Missing data: {self.df.isnull().sum().sum()} cells")
        
        # Bank-wise count
        print("\n🏦 Reviews per bank:")
        for bank in self.df['bank'].unique():
            count = len(self.df[self.df['bank'] == bank])
            print(f"  {bank}: {count} reviews")
        
        # Data quality check
        missing_pct = (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        print(f"📈 Data quality: {missing_pct:.2f}% missing data")
        
        if missing_pct < 5:
            print(" KPI ACHIEVED: <5% missing data")
        else:
            print(" KPI NOT MET: >5% missing data")
    
    def process(self):
        """Run complete preprocessing pipeline"""
        print("🚀 Starting data preprocessing...")
        
        if not self.load_data():
            return False
        
        self.remove_duplicates()
        self.handle_missing_data() 
        self.normalize_dates()
        self.clean_text()
        self.select_final_columns()
        self.save_clean_data()
        self.generate_report()
        
        return True


def main():
    preprocessor = ReviewPreprocessor()
    success = preprocessor.process()
    
    if success:
        print("\n Preprocessing completed successfully!")
        return preprocessor.df
    else:
        print("\n Preprocessing failed!")
        return None


if __name__ == "__main__":
    processed_df = main()