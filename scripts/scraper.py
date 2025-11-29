"""
Google Play Store Review Scraper for Ethiopian Banks - TASK 1
Enhanced with robust retry mechanism and error handling
"""

import sys
import os

# Simple fix - go up one level from scripts directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from google_play_scraper import app, reviews, Sort
import time
from tqdm import tqdm
from datetime import datetime
from config import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS, create_data_directories


class EthiopianBankScraper:
    """Enhanced scraper with robust error handling and retry logic"""
    
    def __init__(self):
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES
        self.config = SCRAPING_CONFIG
        self.app_info_data = []
        
        # CREATE DIRECTORIES when scraper initializes
        self._create_directories()
        
    def _create_directories(self):
        """Create necessary data directories"""
        print("📁 Creating data directories...")
        try:
            create_data_directories()  # Use the function from config
            print(" Directories ready")
        except Exception as e:
            print(f" Directory creation failed: {e}")
            # Fallback: create directories manually
            os.makedirs('data/raw', exist_ok=True)
            os.makedirs('data/processed', exist_ok=True)
            print(" Directories created (fallback)")
        
    def scrape_with_retry(self, app_id, bank_name):
        """
        Scrape reviews with retry mechanism for reliability
        """
        for attempt in range(self.config['max_retries']):
            try:
                print(f"   Attempt {attempt + 1}/{self.config['max_retries']} for {bank_name}...")
                
                reviews_data, continuation_token = reviews(
                    app_id,
                    lang=self.config['lang'],
                    country=self.config['country'], 
                    sort=Sort.NEWEST,
                    count=self.config['reviews_per_bank']
                )
                
                print(f"    Success on attempt {attempt + 1}")
                return reviews_data
                
            except Exception as e:
                print(f"    Attempt {attempt + 1} failed: {str(e)}")
                
                # If this wasn't the last attempt, wait before retrying
                if attempt < self.config['max_retries'] - 1:
                    wait_time = self.config['retry_delay'] * (attempt + 1)  # Exponential backoff
                    print(f"    Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"    All {self.config['max_retries']} attempts failed for {bank_name}")
                    return []
        
        return []  # Should never reach here, but for safety
    
    def collect_app_info(self):
        """Collect app information with error handling"""
        print("📱 Collecting App Information...")
        print("-" * 50)
        
        for bank_code, app_id in self.app_ids.items():
            try:
                app_info = app(app_id)
                
                app_data = {
                    'bank_code': bank_code,
                    'bank_name': self.bank_names[bank_code],
                    'app_id': app_id,
                    'app_name': app_info.get('title', 'N/A'),
                    'description': app_info.get('description', '')[:200] + '...',
                    'current_rating': app_info.get('score', 0),
                    'ratings_count': app_info.get('ratings', 0),
                    'reviews_count': app_info.get('reviews', 0),
                    'installs': app_info.get('installs', 'N/A'),
                    'version': app_info.get('version', 'N/A'),
                    'updated_date': app_info.get('updated', None),
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                self.app_info_data.append(app_data)
                print(f" {self.bank_names[bank_code]}: {app_data['app_name']}")
                print(f"   Rating: {app_data['current_rating']}/5 | Reviews: {app_data['reviews_count']}")
                
            except Exception as e:
                print(f" {self.bank_names[bank_code]}: App info failed - {e}")
                # Add placeholder for failed apps
                self.app_info_data.append({
                    'bank_code': bank_code,
                    'bank_name': self.bank_names[bank_code],
                    'app_id': app_id,
                    'app_name': 'Unknown - Access Failed',
                    'current_rating': 0,
                    'reviews_count': 0,
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'error': str(e)
                })
    
    def save_app_info(self):
        """Save app information to CSV"""
        if self.app_info_data:
            app_info_df = pd.DataFrame(self.app_info_data)
            app_info_df.to_csv(DATA_PATHS['app_info'], index=False)
            print(f"💾 App info saved to: {DATA_PATHS['app_info']}")
            return True
        return False
    
    def scrape_single_bank(self, bank_code, app_id):
        """Scrape reviews for a single bank with retry mechanism"""
        try:
            # Get app info
            app_info = app(app_id)
            actual_app_name = app_info.get('title', 'Unknown App')
            
            print(f"📥 Scraping {self.bank_names[bank_code]}...")
            
            # Use retry mechanism for scraping
            reviews_data = self.scrape_with_retry(app_id, self.bank_names[bank_code])
            
            if not reviews_data:
                print(f" No reviews collected for {self.bank_names[bank_code]}")
                return []
            
            # Process reviews
            processed_reviews = []
            for review in reviews_data:
                processed_reviews.append({
                    'review_id': review.get('reviewId', ''),
                    'review_text': review.get('content', ''),
                    'rating': review.get('score', 0),
                    'review_date': review.get('at', datetime.now()),
                    'user_name': review.get('userName', 'Anonymous'),
                    'thumbs_up': review.get('thumbsUpCount', 0),
                    'app_version': review.get('reviewCreatedVersion', 'N/A'),
                    'bank_code': bank_code,
                    'bank_name': self.bank_names[bank_code],
                    'app_name': actual_app_name,
                    'source': 'Google Play',
                    'original_length': len(review.get('content', '')),
                    'has_reply': review.get('replyContent') is not None
                })
            
            print(f" {self.bank_names[bank_code]}: Collected {len(processed_reviews)} raw reviews")
            return processed_reviews
            
        except Exception as e:
            print(f" Critical error scraping {self.bank_names[bank_code]}: {e}")
            return []
    
    def scrape_all_banks(self):
        """Scrape reviews for all banks with comprehensive error handling"""
        all_reviews = []
        successful_banks = 0
        
        print("\n STARTING ROBUST REVIEW SCRAPING")
        print("=" * 50)
        print(f"Configuration: {self.config['reviews_per_bank']} reviews/bank, {self.config['max_retries']} retries")
        print("=" * 50)
        
        # Collect app info first
        self.collect_app_info()
        self.save_app_info()
        
        # Scrape each bank
        for bank_code, app_id in tqdm(self.app_ids.items(), desc="Scraping Banks"):
            bank_reviews = self.scrape_single_bank(bank_code, app_id)
            
            if bank_reviews:  # Only count if we got reviews
                all_reviews.extend(bank_reviews)
                successful_banks += 1
            else:
                print(f"  Skipping {self.bank_names[bank_code]} - no reviews collected")
            
            # Polite delay between banks
            time.sleep(2)
        
        # Create DataFrame and save
        if all_reviews:
            comprehensive_df = pd.DataFrame(all_reviews)
            comprehensive_df.to_csv(DATA_PATHS['raw_reviews'], index=False)
            self._generate_scraping_summary(comprehensive_df, successful_banks)
            return comprehensive_df
        else:
            print(" CRITICAL: No reviews collected from any bank!")
            return pd.DataFrame()
    
    def _generate_scraping_summary(self, df, successful_banks):
        """Generate detailed scraping summary"""
        print("\n" + "=" * 50)
        print("📊 ROBUST SCRAPING SUMMARY")
        print("=" * 50)
        
        total_reviews = len(df)
        print(f"Successful banks: {successful_banks}/{len(self.app_ids)}")
        print(f"Total Raw Reviews: {total_reviews}")
        
        print("\n🏦 Raw Reviews per Bank:")
        for bank_name in df['bank_name'].unique():
            bank_count = len(df[df['bank_name'] == bank_name])
            status = "✅" if bank_count >= 400 else "⚠️ "
            print(f"  {status} {bank_name}: {bank_count} reviews")
        
        # Success rate calculation
        success_rate = (successful_banks / len(self.app_ids)) * 100
        print(f"\n📈 Success Rate: {success_rate:.1f}% of banks")
        
        if success_rate == 100:
            print(" All banks scraped successfully!")
        else:
            print("  Some banks failed - check errors above")


def main():
    """Main execution function with top-level error handling"""
    try:
        scraper = EthiopianBankScraper()
        df = scraper.scrape_all_banks()
        
        if df.empty:
            print("\n SCRAPING FAILED: No data collected")
            sys.exit(1)
        else:
            print("\n SCRAPING COMPLETED SUCCESSFULLY!")
            return df
            
    except Exception as e:
        print(f"\n UNEXPECTED ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    reviews_df = main()