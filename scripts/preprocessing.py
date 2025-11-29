"""
Data Preprocessing for Ethiopian Bank Reviews - TASK 1
Enhanced with smart language filtering and comprehensive cleaning
"""

import sys
import os
import pandas as pd
import numpy as np
import re
from datetime import datetime

# Add parent directory to path for config import
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import DATA_PATHS


class ReviewPreprocessor:
    """Enhanced preprocessor with smart Amharic/Arabic filtering"""
    
    def __init__(self):
        self.input_path = DATA_PATHS['raw_reviews']
        self.output_path = DATA_PATHS['processed_reviews']
        self.df = None
        self.stats = {
            'original_count': 0,
            'duplicates_removed': 0,
            'language_filtered': 0,
            'missing_removed': 0,
            'invalid_ratings': 0,
            'final_count': 0
        }
    
    def load_data(self):
        """Load raw reviews data"""
        print("📥 Loading raw data...")
        try:
            self.df = pd.read_csv(self.input_path)
            self.stats['original_count'] = len(self.df)
            print(f" Loaded {len(self.df)} raw reviews")
            
            # Show initial data overview
            print(f"   Columns: {list(self.df.columns)}")
            print(f"   Banks: {self.df['bank_name'].unique()}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load data: {e}")
            return False
    
    def remove_duplicates_comprehensive(self):
        """Remove duplicates using multiple criteria"""
        print("\n🧹 Removing duplicates...")
        
        before = len(self.df)
        
        # Strategy 1: Exact duplicates on multiple fields
        self.df = self.df.drop_duplicates(
            subset=['review_text', 'review_date', 'user_name'], 
            keep='first'
        )
        
        removed = before - len(self.df)
        self.stats['duplicates_removed'] = removed
        print(f" Removed {removed} duplicate reviews")
    
    def _text_similarity(self, text1, text2):
        """Calculate simple text similarity ratio"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def handle_missing_values(self):
        """Handle missing values intelligently"""
        print("\n Handling missing values...")
        
        before = len(self.df)
        
        # Check missing values
        missing_data = self.df.isnull().sum()
        print("Missing values per column:")
        for col, count in missing_data.items():
            if count > 0:
                pct = (count / len(self.df)) * 100
                print(f"   {col}: {count} ({pct:.1f}%)")
        
        # Remove rows with critical missing data
        critical_cols = ['review_text', 'rating', 'review_date', 'bank_name']
        self.df = self.df.dropna(subset=critical_cols)
        
        # Remove empty reviews
        self.df = self.df[self.df['review_text'].str.strip() != '']
        
        # Fill non-critical missing values
        self.df['user_name'] = self.df['user_name'].fillna('Anonymous')
        self.df['thumbs_up'] = self.df['thumbs_up'].fillna(0)
        self.df['app_version'] = self.df['app_version'].fillna('Unknown')
        
        removed = before - len(self.df)
        self.stats['missing_removed'] = removed
        print(f" Removed {removed} reviews with missing critical data")
    
    def smart_language_filter(self):  # FIXED: Proper indentation
        """
        Enhanced filtering for the specific garbage patterns in your data
        """
        print("\n🌍 Applying targeted language filtering...")
        
        before_count = len(self.df)
        keep_mask = []
        
        # SPECIFIC GARBAGE PATTERNS FROM YOUR EXAMPLES
        garbage_patterns = [
        # Pattern 1: Mixed Amharic garbage
        r'^[áŒ¥áˆ©áŠá‹áŒáŠ•áˆ‹á‹­áŠ á‹µáˆ­áŒŽá‹«á‰†áˆáˆˆáŠ•áŒá‹µáˆµáˆ«]+$',
        r'^[áŒ­áˆµáˆ˜áˆáŠ­áˆ«á‰½á‹áŠ¥áŠ“áŠ á‹­áŒˆáŠ“áŠáˆá¢á‰ áŒ£áˆá‹¨áˆšá‹«áˆµáŒ áˆ‹]+$',
        r'^[áŠ áˆªá‹áŠá‹‰áŠáŒˆáˆ­áŒáŠ•á‰ áŒ£áˆá‹¨á‰†á‹¨á‹‰áŠ•á‹¨áˆšá‹«áˆ³á‹­]+$',
        r'maaliif daddafee install gaafata',
        r'Nuuroo usmaan gaamilcom',
        
        # Pattern 2: Emoji-only or excessive emoji
        r'^[ðŸ‘ŒðŸ˜˜ðŸ‘ðŸ˜ŠðŸ¥°\U0001F600-\U0001F64F]+$',
        r'^[âœŒï¸â™¥ï¸ðŸ˜¡ðŸ‡ªðŸ‡¹]+$',
        
        # Pattern 3: Symbol/number garbage
        r'^[z,MKT 20_\.!_!8+\+\â…"â…•]+$',
        r'^[0-9\s\.\_\!\+]+$',
        
        
        # Pattern 4: Specific Amharic garbage patterns you provided
        r'á‰ áŒ£áˆ áŠ áˆªá! áŠ¨á‰€á‹µáˆžá‹',
        r'áˆˆ áŠ•áŒá‹µ áˆµáˆ«áˆˆ áŠ•áŒá‹µ áˆµáˆ«',
        r'áˆáŒ£áŠ• áŠ¥áŠ“ áˆáˆ­áŒ¥ á‰£áŠ•áŠ­ áŠá‹',
        r'Ø§Ù„Ø³Ù„Ø§Ù… Ø¹Ù„ÙŠÙƒÙ… ÙˆØ±Ø­Ù…Ø© Ø§Ù„Ù„Ù‡ ÙˆØ¨Ø±ÙƒØ§ØªÙ‡',
            
            # Pattern 5: Mixed garbage with angle brackets
            r'^<>.+$',
            
            # Pattern 5: Very short or repetitive
            r'^.{0,2}$',  # 0-2 characters
            r'^(\w\W*){1,3}$',  # 1-3 words with symbols
        ]
        
        # Amharic Unicode range for detection
        amharic_range = r'[\u1200-\u137F]'
        
        removed_categories = {
            'short': 0,
            'garbage': 0,
            'amharic_only': 0,
            'single_word': 0,
            'emoji_only': 0
        }
        
        for idx, row in self.df.iterrows():
            review_text = str(row['review_text']).strip()
            
            # Skip empty or very short
            if len(review_text) < 3:
                keep_mask.append(False)
                removed_categories['short'] += 1
                continue
            
            # Check for specific garbage patterns
            is_garbage = any(re.search(pattern, review_text, re.IGNORECASE) 
                           for pattern in garbage_patterns)
            if is_garbage:
                keep_mask.append(False)
                removed_categories['garbage'] += 1
                continue
            
            # Check for Amharic-only content (no English)
            has_amharic = re.search(amharic_range, review_text)
            english_words = len(re.findall(r'\b[a-zA-Z]{3,}\b', review_text))
            
            if has_amharic and english_words == 0:
                keep_mask.append(False)
                removed_categories['amharic_only'] += 1
                continue
            
            # Check for single word reviews without context
            words = re.findall(r'\b\w+\b', review_text)
            if len(words) <= 1 and len(review_text) < 4:
                keep_mask.append(False)
                removed_categories['single_word'] += 1
                continue
            
            # Check for emoji-only reviews
            emoji_only = re.match(r'^[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]+$', review_text)
            if emoji_only:
                keep_mask.append(False)
                removed_categories['emoji_only'] += 1
                continue
            
            # KEEP the review if it passed all filters
            keep_mask.append(True)
        
        # Apply the filter
        self.df = self.df[keep_mask]
        total_removed = before_count - len(self.df)
        
        # Detailed removal report
        print(f" Targeted filtering completed:")
        for category, count in removed_categories.items():
            if count > 0:
                print(f"   {category}: {count}")
        print(f"   Kept {len(self.df)} meaningful reviews")
        
        self.stats['language_filtered'] = total_removed
    
    def normalize_dates(self):  # ADDED: Missing method
        """Normalize dates to YYYY-MM-DD format"""
        print("\n📅 Normalizing dates...")
        
        try:
            # Convert to datetime and format as YYYY-MM-DD
            self.df['review_date'] = pd.to_datetime(self.df['review_date']).dt.strftime('%Y-%m-%d')
            print(" Dates normalized to YYYY-MM-DD")
            
            # Show date range
            date_range = f"{self.df['review_date'].min()} to {self.df['review_date'].max()}"
            print(f"📆 Date range: {date_range}")
            
        except Exception as e:
            print(f" Error normalizing dates: {e}")
    
    def clean_text_content(self):
        """Clean review text while preserving meaning"""
        print("\n✨ Cleaning review text...")
        
        def clean_single_text(text):
            if pd.isna(text) or text == '':
                return ""
            
            text = str(text).strip()
            
            # Replace multiple spaces/tabs/newlines with single space
            text = re.sub(r'\s+', ' ', text)
            
            # Remove excessive punctuation (keep basic .!?)
            text = re.sub(r'[!?]{3,}', '!', text)  # !!! -> !
            text = re.sub(r'\.{3,}', '...', text)  # ...... -> ...
            
            # Clean up common issues but preserve content
            text = text.replace('&amp;', '&')
            text = text.replace('&quot;', '"')
            text = text.replace('&lt;', '<')
            text = text.replace('&gt;', '>')
            
            return text.strip()
        
        # Apply cleaning
        self.df['review_text'] = self.df['review_text'].apply(clean_single_text)
        
        # Add text length for analysis
        self.df['text_length'] = self.df['review_text'].str.len()
        
        print(" Text cleaning completed")
        print(f"   Average length: {self.df['text_length'].mean():.1f} characters")
    
    def validate_ratings(self):
        """Validate and clean rating values"""
        print("\n⭐ Validating ratings...")
        
        before = len(self.df)
        
        # Check for invalid ratings
        invalid_mask = ~self.df['rating'].between(1, 5)
        invalid_count = invalid_mask.sum()
        
        if invalid_count > 0:
            print(f"  Found {invalid_count} invalid ratings:")
            invalid_ratings = self.df[invalid_mask]['rating'].value_counts()
            for rating, count in invalid_ratings.items():
                print(f"   Rating {rating}: {count} reviews")
            
            # Remove invalid ratings
            self.df = self.df[~invalid_mask]
            print(f" Removed {invalid_count} invalid ratings")
        else:
            print(" All ratings are valid (1-5 stars)")
        
        self.stats['invalid_ratings'] = invalid_count
    
    def select_final_columns(self):
        """
        Select only Task 1 required columns for final output
        review, rating, date, bank, source
        """
        print("\n🎯 Selecting required columns...")
        
        # Map from comprehensive columns to Task 1 required columns
        column_mapping = {
            'review_text': 'review',
            'review_date': 'date', 
            'bank_name': 'bank'
        }
        
        # Apply mapping
        self.df = self.df.rename(columns=column_mapping)
        
        # Ensure we have the exact required columns
        required_columns = ['review', 'rating', 'date', 'bank', 'source']
        
        # Keep only required columns that exist
        available_columns = [col for col in required_columns if col in self.df.columns]
        self.df = self.df[available_columns]
        
        print(" Final columns selected:")
        for col in self.df.columns:
            print(f"   - {col}")
    
    def validate_data_quality(self):
        """Validate final data meets Task 1 requirements"""
        print("\n Validating final data quality...")
        
        # Final missing data check
        missing_final = self.df.isnull().sum().sum()
        total_cells = len(self.df) * len(self.df.columns)
        missing_percentage = (missing_final / total_cells) * 100 if total_cells > 0 else 0
        
        self.stats['final_count'] = len(self.df)
        self.stats['missing_percentage'] = missing_percentage
        
        print(f"📊 Final data quality:")
        print(f"   Total reviews: {len(self.df)}")
        print(f"   Missing data: {missing_percentage:.2f}%")
        
        
        if missing_percentage < 5:
            print(" ACHIEVED: <5% missing data")
        else:
            print(" NOT MET: >5% missing data")
    
    def save_processed_data(self):
        """Save the cleaned Task 1 data"""
        print("\n💾 Saving processed data...")
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            # Save to CSV
            self.df.to_csv(self.output_path, index=False)
            print(f" Processed data saved to: {self.output_path}")
            return True
            
        except Exception as e:
            print(f" Failed to save data: {e}")
            return False
    
    def generate_comprehensive_report(self):
        """Generate comprehensive Task 1 preprocessing report"""
        print("\n" + "=" * 60)
        print("📋 TASK 1 - COMPREHENSIVE PREPROCESSING REPORT")
        print("=" * 60)
        
        # Processing pipeline summary
        print(f"\n🔄 PROCESSING PIPELINE SUMMARY:")
        print(f"   Original raw reviews: {self.stats['original_count']}")
        print(f"   Duplicates removed: {self.stats['duplicates_removed']}")
        print(f"   Language filtered: {self.stats['language_filtered']}")
        print(f"   Missing data removed: {self.stats['missing_removed']}")
        print(f"   Invalid ratings: {self.stats['invalid_ratings']}")
        print(f"   FINAL CLEAN REVIEWS: {self.stats['final_count']}")
        
        retention_rate = (self.stats['final_count'] / self.stats['original_count']) * 100
        print(f"   Data retention: {retention_rate:.1f}%")
        
        # Bank-wise final count
        print(f"\n🏦 FINAL REVIEWS PER BANK:")
        bank_counts = self.df['bank'].value_counts()
        for bank, count in bank_counts.items():
            status = " TARGET MET" if count >= 400 else "⚠️ NEEDS MORE"
            print(f"   {bank}: {count} reviews - {status}")
        
        # Rating distribution
        print(f"\n⭐ RATING DISTRIBUTION:")
        rating_counts = self.df['rating'].value_counts().sort_index(ascending=False)
        for rating, count in rating_counts.items():
            percentage = (count / len(self.df)) * 100
            stars = '⭐' * int(rating)
            print(f"   {stars} ({rating}): {count} reviews ({percentage:.1f}%)")
        
        # Text statistics
        print(f"\n📝 TEXT STATISTICS:")
        print(f"   Average length: {self.df['review'].str.len().mean():.1f} chars")
        print(f"   Shortest review: {self.df['review'].str.len().min()} chars")
        print(f"   Longest review: {self.df['review'].str.len().max()} chars")
        
        # Sample of cleaned reviews
        print(f"\n SAMPLE CLEANED REVIEWS:")
        samples = self.df.head(3)
        for idx, row in samples.iterrows():
            preview = row['review'][:100] + '...' if len(row['review']) > 100 else row['review']
            print(f"   ⭐{row['rating']} - {preview}")
    
    def process(self):
        """Run complete enhanced preprocessing pipeline"""
        print("🚀 STARTING ENHANCED PREPROCESSING PIPELINE")
        print("=" * 50)
        
        if not self.load_data():
            return False
        
        # Enhanced processing steps
        self.remove_duplicates_comprehensive()
        self.handle_missing_values()
        self.smart_language_filter()
        self.normalize_dates()
        self.clean_text_content()
        self.validate_ratings()
        self.select_final_columns()
        self.validate_data_quality()
        
        if self.save_processed_data():
            self.generate_comprehensive_report()
            return True
        
        return False


def main():
    """Main execution function"""
    preprocessor = ReviewPreprocessor()
    success = preprocessor.process()
    
    if success:
        print("\n PREPROCESSING COMPLETED SUCCESSFULLY!")
        return preprocessor.df
    else:
        print("\n PREPROCESSING FAILED!")
        return None


if __name__ == "__main__":
    processed_df = main()