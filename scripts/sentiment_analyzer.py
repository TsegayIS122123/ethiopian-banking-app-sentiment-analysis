"""
Enhanced Sentiment Analysis for Ethiopian Bank Reviews - TASK 2
Using DistilBERT for high-accuracy sentiment classification
"""

import pandas as pd
import numpy as np
from transformers import pipeline
import torch
from tqdm import tqdm
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_PATHS

class SentimentAnalyzer:
    """Enhanced sentiment analysis with DistilBERT and confidence scoring"""
    
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        print("🤖 Loading DistilBERT sentiment model...")
        
        # Initialize the sentiment pipeline
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=model_name,
            tokenizer=model_name,
            truncation=True,
            max_length=512,
            device=0 if torch.cuda.is_available() else -1  # Use GPU if available
        )
        
        self.stats = {
            'total_reviews': 0,
            'analyzed_reviews': 0,
            'failed_analysis': 0
        }
    
    def analyze_sentiment_batch(self, texts, batch_size=32):
        """Analyze sentiment in batches for efficiency"""
        results = []
        
        for i in tqdm(range(0, len(texts), batch_size), desc="Analyzing Sentiment"):
            batch = texts[i:i + batch_size]
            try:
                batch_results = self.sentiment_pipeline(batch)
                results.extend(batch_results)
            except Exception as e:
                print(f"❌ Batch {i//batch_size + 1} failed: {e}")
                # Add neutral sentiment for failed batches
                results.extend([{'label': 'NEUTRAL', 'score': 0.5}] * len(batch))
                self.stats['failed_analysis'] += len(batch)
        
        return results
    
    def apply_neutral_threshold(self, label, score):
        """Apply neutral threshold to create 3-class system"""
        if 0.4 <= score <= 0.6:
            return 'NEUTRAL', score
        else:
            return label, score
    
    def sentiment_to_numeric(self, label, score):
        """Convert sentiment to numerical scale for aggregation (-1 to +1)"""
        if label == 'POSITIVE':
            return score  # Positive values: 0.0 to 1.0
        elif label == 'NEGATIVE':
            return -score  # Negative values: -1.0 to 0.0
        else:  # NEUTRAL
            return 0.0
    
    def add_sentiment_to_dataframe(self, df, text_column='review'):
        """Add sentiment labels and scores to dataframe"""
        print("🎯 Starting sentiment analysis...")
        
        self.stats['total_reviews'] = len(df)
        
        # Get texts for analysis
        texts = df[text_column].astype(str).tolist()
        
        # Analyze sentiment
        sentiment_results = self.analyze_sentiment_batch(texts)
        
        # Extract and process labels and scores
        sentiment_labels = []
        sentiment_scores = []
        sentiment_numeric = []
        
        for result in sentiment_results:
            label = result['label'].upper()  # Ensure uppercase
            score = result['score']
            
            # Apply neutral threshold
            final_label, final_score = self.apply_neutral_threshold(label, score)
            
            sentiment_labels.append(final_label)
            sentiment_scores.append(final_score)
            sentiment_numeric.append(self.sentiment_to_numeric(final_label, final_score))
        
        # Add to dataframe
        df['sentiment_label'] = sentiment_labels
        df['sentiment_score'] = sentiment_scores
        df['sentiment_numeric'] = sentiment_numeric
        
        self.stats['analyzed_reviews'] = len(sentiment_results)
        
        return df
    
    def get_sentiment_summary(self, df):
        """Generate comprehensive sentiment summary by bank and rating"""
        print("\n📊 Generating sentiment summary...")
        
        # Summary by bank
        bank_sentiment = df.groupby('bank').agg({
            'sentiment_numeric': ['mean', 'count'],
            'sentiment_label': lambda x: x.value_counts().to_dict()
        }).round(3)
        
        # Summary by rating
        rating_sentiment = df.groupby('rating').agg({
            'sentiment_numeric': ['mean', 'count'],
            'sentiment_label': lambda x: x.value_counts().to_dict()
        }).round(3)
        
        # Combined bank + rating summary
        bank_rating_sentiment = df.groupby(['bank', 'rating']).agg({
            'sentiment_numeric': 'mean',
            'sentiment_score': 'mean',
            'sentiment_label': 'count'
        }).round(3)
        
        return {
            'bank_summary': bank_sentiment,
            'rating_summary': rating_sentiment,
            'bank_rating_summary': bank_rating_sentiment
        }
    
    def save_sentiment_results(self, df):
        """Save results with sentiment analysis"""
        output_path = DATA_PATHS['sentiment_results']
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        print(f"💾 Sentiment results saved to: {output_path}")
        
        return output_path
    
    def generate_sentiment_report(self, df):
        """Generate comprehensive sentiment analysis report"""
        print("\n" + "=" * 60)
        print("📋 TASK 2 - SENTIMENT ANALYSIS REPORT")
        print("=" * 60)
        
        print(f"\n📈 OVERALL SENTIMENT DISTRIBUTION:")
        overall_sentiment = df['sentiment_label'].value_counts()
        for sentiment, count in overall_sentiment.items():
            percentage = (count / len(df)) * 100
            print(f"   {sentiment}: {count} reviews ({percentage:.1f}%)")
        
        print(f"\n🏦 SENTIMENT BY BANK:")
        for bank in df['bank'].unique():
            bank_data = df[df['bank'] == bank]
            total = len(bank_data)
            avg_sentiment = bank_data['sentiment_numeric'].mean()
            
            sentiment_counts = bank_data['sentiment_label'].value_counts()
            print(f"\n   {bank} (Avg: {avg_sentiment:.3f}):")
            for sentiment in ['POSITIVE', 'NEUTRAL', 'NEGATIVE']:
                count = sentiment_counts.get(sentiment, 0)
                percentage = (count / total) * 100
                print(f"     {sentiment}: {count} ({percentage:.1f}%)")
        
        print(f"\n⭐ SENTIMENT vs RATING CORRELATION:")
        for rating in sorted(df['rating'].unique()):
            rating_data = df[df['rating'] == rating]
            avg_sentiment = rating_data['sentiment_numeric'].mean()
            sentiment_dist = rating_data['sentiment_label'].value_counts()
            print(f"   ⭐{rating}: Avg sentiment {avg_sentiment:.3f}")
            for label, count in sentiment_dist.items():
                print(f"        {label}: {count} reviews")
        
        print(f"\n📊 ANALYSIS STATISTICS:")
        print(f"   Total reviews analyzed: {self.stats['analyzed_reviews']}")
        print(f"   Failed analyses: {self.stats['failed_analysis']}")
        success_rate = (self.stats['analyzed_reviews'] / self.stats['total_reviews']) * 100
        print(f"   Success rate: {success_rate:.1f}%")

def main():
    """Main execution function for sentiment analysis"""
    try:
        # Load preprocessed data from Task 1
        print("📥 Loading preprocessed data...")
        df = pd.read_csv(DATA_PATHS['processed_reviews'])
        print(f"   Loaded {len(df)} reviews")
        
        # Add review_id if not present
        if 'review_id' not in df.columns:
            df['review_id'] = [f"REVIEW_{i:04d}" for i in range(1, len(df)+1)]
            print("   Added review_id column")
        
        # Initialize analyzer
        analyzer = SentimentAnalyzer()
        
        # Perform sentiment analysis
        df_with_sentiment = analyzer.add_sentiment_to_dataframe(df)
        
        # Generate reports
        analyzer.generate_sentiment_report(df_with_sentiment)
        
        # Save results
        output_path = analyzer.save_sentiment_results(df_with_sentiment)
        
        print(f"\n✅ SENTIMENT ANALYSIS COMPLETED!")
        return df_with_sentiment
        
    except Exception as e:
        print(f"❌ Sentiment analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    sentiment_df = main()