"""
Enhanced Thematic Analysis for Ethiopian Bank Reviews - TASK 2
Using TF-IDF and rule-based clustering for theme identification
"""

import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter, defaultdict
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_PATHS

class ThemeAnalyzer:
    """Enhanced thematic analysis with TF-IDF and rule-based clustering"""
    
    def __init__(self):
        print("🔍 Setting up thematic analysis...")
        
        # Define comprehensive theme patterns for Ethiopian banking context
        self.theme_patterns = {
            'Login & Access Issues': [
                'login', 'password', 'access', 'account', 'verify', 'authentication',
                'sign in', 'log in', 'cannot login', 'login problem', 'access denied',
                'unable to login', 'wrong password', 'forgot password'
            ],
            'Transaction Problems': [
                'transfer', 'transaction', 'payment', 'send money', 'receive money',
                'failed transaction', 'transaction failed', 'money transfer', 'payment failed',
                'transfer failed', 'cannot transfer', 'pending transaction', 'stuck transaction'
            ],
            'App Performance & Speed': [
                'slow', 'fast', 'speed', 'loading', 'lag', 'crash', 'freeze', 'hang',
                'responsive', 'performance', 'crashes', 'freezes', 'not responding',
                'takes long', 'very slow', 'too slow', 'loading time', 'response time'
            ],
            'User Interface & Experience': [
                'interface', 'design', 'layout', 'navigation', 'button', 'menu',
                'user friendly', 'easy to use', 'complicated', 'confusing', 'simple',
                'intuitive', 'beautiful', 'ugly', 'modern', 'outdated', 'cluttered'
            ],
            'Customer Support': [
                'support', 'help', 'service', 'response', 'contact', 'assistance',
                'customer service', 'help desk', 'no response', 'poor support',
                'bad service', 'slow response', 'unhelpful', 'customer care'
            ],
            'Security Concerns': [
                'security', 'safe', 'secure', 'hack', 'privacy', 'protection',
                'data security', 'personal information', 'secure transaction',
                'trust', 'fraud', 'scam', 'hacked', 'privacy concern'
            ],
            'Feature Requests': [
                'should', 'would', 'could', 'add', 'feature', 'want', 'need',
                'please add', 'missing feature', 'suggestion', 'recommend',
                'wish', 'hope', 'improve', 'enhancement', 'new feature'
            ],
            'Network & Connectivity': [
                'network', 'connection', 'internet', 'connect', 'offline',
                'no internet', 'connection problem', 'network error',
                'disconnect', 'connection lost', 'poor connection'
            ]
        }
        
        self.stats = {
            'total_reviews': 0,
            'reviews_with_themes': 0,
            'themes_identified': 0
        }
    
    def advanced_text_clean(self, text):
        """Enhanced text preprocessing for thematic analysis"""
        if pd.isna(text):
            return ""
        
        text = str(text).lower().strip()
        
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_keywords_tfidf(self, texts, max_features=100):
        """Extract keywords using TF-IDF with n-grams"""
        print("   Extracting keywords with TF-IDF...")
        
        # Create TF-IDF vectorizer with n-grams
        vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 3),  # Include unigrams, bigrams, and trigrams
            min_df=2,  # Ignore terms that appear in only 1 document
            max_df=0.8  # Ignore terms that appear in more than 80% of documents
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get TF-IDF scores
            scores = np.array(tfidf_matrix.mean(axis=0)).flatten()
            
            # Create keyword-score pairs
            keyword_scores = list(zip(feature_names, scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            print(f"   Top 10 keywords: {[k[0] for k in keyword_scores[:10]]}")
            return keyword_scores
            
        except Exception as e:
            print(f"   TF-IDF extraction failed: {e}")
            return []
    
    def identify_themes_in_review(self, review_text):
        """Identify themes in a single review using pattern matching"""
        themes_found = []
        cleaned_text = self.advanced_text_clean(review_text)
        
        if not cleaned_text or len(cleaned_text) < 10:
            return themes_found
        
        # Check each theme pattern
        for theme, keywords in self.theme_patterns.items():
            # Check for keyword matches in cleaned text
            theme_matches = sum(1 for keyword in keywords if keyword in cleaned_text)
            
            if theme_matches >= 1:
                themes_found.append(theme)
        
        return list(set(themes_found))  # Remove duplicates
    
    def analyze_themes_by_bank(self, df, text_column='review'):
        """Perform comprehensive thematic analysis by bank"""
        print("🎯 Starting thematic analysis...")
        
        self.stats['total_reviews'] = len(df)
        
        # Identify themes for each review
        print("   Processing reviews for theme identification...")
        df['identified_themes'] = df[text_column].apply(self.identify_themes_in_review)
        
        # Count themes identified
        theme_counts = []
        for themes in df['identified_themes']:
            theme_counts.extend(themes)
        
        self.stats['themes_identified'] = len(theme_counts)
        self.stats['reviews_with_themes'] = len(df[df['identified_themes'].str.len() > 0])
        
        # Analyze themes by bank
        bank_themes = defaultdict(Counter)
        
        for idx, row in df.iterrows():
            bank = row['bank']
            themes = row['identified_themes']
            
            for theme in themes:
                bank_themes[bank][theme] += 1
        
        return df, dict(bank_themes)
    
    def generate_theme_report(self, df, bank_themes):
        """Generate comprehensive thematic analysis report"""
        print("\n" + "=" * 60)
        print("📋 TASK 2 - THEMATIC ANALYSIS REPORT")
        print("=" * 60)
        
        print(f"\n📊 THEME IDENTIFICATION SUMMARY:")
        print(f"   Total reviews analyzed: {self.stats['total_reviews']}")
        print(f"   Reviews with identified themes: {self.stats['reviews_with_themes']}")
        print(f"   Total themes identified: {self.stats['themes_identified']}")
        
        coverage_rate = (self.stats['reviews_with_themes'] / self.stats['total_reviews']) * 100
        print(f"   Theme coverage rate: {coverage_rate:.1f}%")
        
        print(f"\n🏦 TOP THEMES BY BANK:")
        for bank, theme_counter in bank_themes.items():
            print(f"\n   {bank}:")
            total_themes = sum(theme_counter.values())
            
            for theme, count in theme_counter.most_common(5):  # Top 5 themes
                percentage = (count / total_themes) * 100 if total_themes > 0 else 0
                print(f"     {theme}: {count} mentions ({percentage:.1f}%)")
        
        print(f"\n🎯 THEME DISTRIBUTION ACROSS BANKS:")
        # Create comparison table
        all_themes = set()
        for theme_counter in bank_themes.values():
            all_themes.update(theme_counter.keys())
        
        comparison_data = []
        for theme in sorted(all_themes):
            row = {'Theme': theme}
            for bank in bank_themes.keys():
                row[bank] = bank_themes[bank].get(theme, 0)
            comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        print(comparison_df.to_string(index=False))
        
        return comparison_df
    
    def extract_representative_reviews(self, df, bank, theme, top_n=3):
        """Extract representative reviews for a specific theme and bank"""
        bank_theme_reviews = df[
            (df['bank'] == bank) & 
            (df['identified_themes'].apply(lambda x: theme in x if x else False))
        ]
        
        if len(bank_theme_reviews) == 0:
            return []
        
        # Return top reviews by sentiment score (most confident examples)
        representative = bank_theme_reviews.nlargest(top_n, 'sentiment_score')
        
        return representative[['review', 'rating', 'sentiment_label']].to_dict('records')
    
    def save_theme_results(self, df):
        """Save results with thematic analysis"""
        output_path = DATA_PATHS['theme_results']
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert themes list to string for CSV
        df_export = df.copy()
        df_export['identified_themes'] = df_export['identified_themes'].apply(
            lambda x: ', '.join(x) if x else 'No themes identified'
        )
        
        df_export.to_csv(output_path, index=False)
        print(f"💾 Thematic analysis results saved to: {output_path}")
        
        return output_path

def main():
    """Main execution function for thematic analysis"""
    try:
        # Load data with sentiment (from Task 2.1)
        print("📥 Loading data with sentiment analysis...")
        sentiment_path = DATA_PATHS['sentiment_results']
        
        if os.path.exists(sentiment_path):
            df = pd.read_csv(sentiment_path)
        else:
            # Fallback to processed data
            df = pd.read_csv(DATA_PATHS['processed_reviews'])
            # Add review_id if not present
            if 'review_id' not in df.columns:
                df['review_id'] = [f"REVIEW_{i:04d}" for i in range(1, len(df)+1)]
        
        print(f"   Loaded {len(df)} reviews")
        
        # Initialize analyzer
        analyzer = ThemeAnalyzer()
        
        # Perform thematic analysis
        df_with_themes, bank_themes = analyzer.analyze_themes_by_bank(df)
        
        # Generate reports
        comparison_df = analyzer.generate_theme_report(df_with_themes, bank_themes)
        
        # Save results
        output_path = analyzer.save_theme_results(df_with_themes)
        
        print(f"\n THEMATIC ANALYSIS COMPLETED!")
        return df_with_themes, bank_themes
        
    except Exception as e:
        print(f" Thematic analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    themes_df, bank_themes_dict = main()