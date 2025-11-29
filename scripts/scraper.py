"""
Google Play Store Review Scraper for Ethiopian Banks
Using OOP approach for better organization
"""

import pandas as pd
from google_play_scraper import app, reviews, Sort
import time
from tqdm import tqdm
from config import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS


class EthiopianBankScraper:
    """Scraper for Ethiopian banking app reviews"""
    
    def __init__(self):
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES
        self.config = SCRAPING_CONFIG
        
    def verify_apps(self):
        """Verify we can access each banking app"""
        print(" Verifying bank apps...")
        
        for bank_code, app_id in self.app_ids.items():
            try:
                app_info = app(app_id)
                print(f" {self.bank_names[bank_code]}:")
                print(f"   - Name: {app_info.get('title', 'N/A')}")
                print(f"   - Installs: {app_info.get('installs', 'N/A')}")
                print(f"   - Rating: {app_info.get('score', 'N/A')}")
            except Exception as e:
                print(f" {self.bank_names[bank_code]}: {e}")
    
    def scrape_bank_reviews(self, bank_code, app_id):
        """Scrape reviews for a single bank"""
        try:
            reviews_data, _ = reviews(
                app_id,
                lang=self.config['lang'],
                country=self.config['country'], 
                sort=Sort.NEWEST,
                count=self.config['reviews_per_bank']
            )
            
            # Process reviews
            processed = []
            for review in reviews_data:
                processed.append({
                    'review_text': review.get('content', ''),
                    'rating': review.get('score', 0),
                    'review_date': review.get('at'),
                    'user_name': review.get('userName', 'Anonymous'),
                    'bank_code': bank_code,
                    'bank_name': self.bank_names[bank_code],
                    'source': 'Google Play Store'
                })
            
            return processed
            
        except Exception as e:
            print(f"Error scraping {bank_code}: {e}")
            return []
    
    def scrape_all_banks(self):
        """Scrape reviews for all three banks"""
        all_reviews = []
        
        print(" Starting to scrape Ethiopian banking apps...")
        
        for bank_code, app_id in tqdm(self.app_ids.items(), desc="Banks"):
            reviews_data = self.scrape_bank_reviews(bank_code, app_id)
            all_reviews.extend(reviews_data)
            
            # Delay between requests
            time.sleep(2)
        
        # Create DataFrame
        df = pd.DataFrame(all_reviews)
        
        # Save raw data
        df.to_csv(DATA_PATHS['raw_reviews'], index=False)
        
        print(f" Scraping completed! Collected {len(df)} reviews")
        
        # Show summary
        self._print_summary(df)
        
        return df
    
    def _print_summary(self, df):
        """Print scraping summary"""
        print("\n SCRAPING SUMMARY:")
        print("=" * 40)
        for bank_code in self.bank_names.keys():
            count = len(df[df['bank_code'] == bank_code])
            print(f"{self.bank_names[bank_code]}: {count} reviews")
        print(f"TOTAL: {len(df)} reviews")


def main():
    """Main function to run the scraper"""
    scraper = EthiopianBankScraper()
    
    # Verify apps first
    scraper.verify_apps()
    
    # Scrape reviews
    df = scraper.scrape_all_banks()
    
    return df


if __name__ == "__main__":
    reviews_df = main()