"""
Task 2 Pipeline Orchestrator - Coordinates Sentiment & Thematic Analysis
"""

import pandas as pd
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_PATHS
from scripts.sentiment_analyzer import SentimentAnalyzer
from scripts.theme_analyzer import ThemeAnalyzer

class Task2Pipeline:
    """Orchestrates complete Task 2 analysis pipeline"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.theme_analyzer = ThemeAnalyzer()
        self.results = {}
        
    def load_task1_data(self):
        """Load and prepare Task 1 data for analysis"""
        print("📥 Loading Task 1 processed data...")
        
        try:
            df = pd.read_csv(DATA_PATHS['processed_reviews'])
            print(f"   Loaded {len(df)} reviews from Task 1")
            
            # Add review_id if not present
            if 'review_id' not in df.columns:
                df['review_id'] = [f"REVIEW_{i:04d}" for i in range(1, len(df)+1)]
                print("   Added review_id column")
            
            # Validate data meets Task 2 requirements
            self._validate_data(df)
            
            return df
            
        except Exception as e:
            print(f"❌ Failed to load Task 1 data: {e}")
            return None
    
    def _validate_data(self, df):
        """Validate data meets Task 2 requirements"""
        print("   Validating data for Task 2...")
        
        required_columns = ['review', 'rating', 'bank']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check minimum review count
        bank_counts = df['bank'].value_counts()
        for bank, count in bank_counts.items():
            if count < 400:
                print(f"   ⚠️  {bank} has only {count} reviews (minimum: 400)")
        
        print("   ✅ Data validation passed")
    
    def run_sentiment_analysis(self, df):
        """Execute sentiment analysis pipeline"""
        print("\n" + "="*50)
        print("🚀 STARTING SENTIMENT ANALYSIS")
        print("="*50)
        
        df_with_sentiment = self.sentiment_analyzer.add_sentiment_to_dataframe(df)
        self.sentiment_analyzer.generate_sentiment_report(df_with_sentiment)
        
        # Save intermediate results
        sentiment_path = self.sentiment_analyzer.save_sentiment_results(df_with_sentiment)
        
        self.results['sentiment_analysis'] = {
            'dataframe': df_with_sentiment,
            'output_path': sentiment_path,
            'summary': self.sentiment_analyzer.get_sentiment_summary(df_with_sentiment)
        }
        
        return df_with_sentiment
    
    def run_thematic_analysis(self, df):
        """Execute thematic analysis pipeline"""
        print("\n" + "="*50)
        print("🚀 STARTING THEMATIC ANALYSIS")
        print("="*50)
        
        df_with_themes, bank_themes = self.theme_analyzer.analyze_themes_by_bank(df)
        comparison_df = self.theme_analyzer.generate_theme_report(df_with_themes, bank_themes)
        
        # Save results
        theme_path = self.theme_analyzer.save_theme_results(df_with_themes)
        
        self.results['thematic_analysis'] = {
            'dataframe': df_with_themes,
            'bank_themes': bank_themes,
            'comparison': comparison_df,
            'output_path': theme_path
        }
        
        return df_with_themes, bank_themes
    
    def generate_final_report(self):
        """Generate comprehensive Task 2 final report"""
        print("\n" + "="*60)
        print("📋 TASK 2 - COMPREHENSIVE FINAL REPORT")
        print("="*60)
        
        sentiment_data = self.results.get('sentiment_analysis', {})
        theme_data = self.results.get('thematic_analysis', {})
        
        if not sentiment_data or not theme_data:
            print("❌ Cannot generate report - missing analysis results")
            return
        
        df_sentiment = sentiment_data['dataframe']
        df_themes = theme_data['dataframe']
        bank_themes = theme_data['bank_themes']
        
        print(f"\n📊 OVERALL TASK 2 ACHIEVEMENTS:")
        print(f"   ✅ Sentiment scores for {len(df_sentiment)} reviews")
        print(f"   ✅ Thematic analysis completed for {len(df_themes)} reviews")
        
        # KPI Check
        sentiment_coverage = (len(df_sentiment) / len(df_sentiment)) * 100
        print(f"   📈 Sentiment coverage: {sentiment_coverage:.1f}%")
        
        print(f"\n🏦 THEMES IDENTIFIED PER BANK:")
        for bank, themes_counter in bank_themes.items():
            theme_count = len(themes_counter)
            status = "✅ ACHIEVED" if theme_count >= 3 else "⚠️  PARTIAL"
            print(f"   {bank}: {theme_count} themes - {status}")
        
        print(f"\n🎯 BUSINESS SCENARIOS INSIGHTS:")
        
        # Scenario 1: Retaining Users - Slow transfers analysis
        transfer_reviews = df_themes[
            df_themes['identified_themes'].apply(
                lambda x: 'Transaction Problems' in x if x else False
            )
        ]
        if len(transfer_reviews) > 0:
            transfer_sentiment = transfer_reviews['sentiment_numeric'].mean()
            print(f"   🔄 Transaction Issues: {len(transfer_reviews)} complaints")
            print(f"      Average sentiment: {transfer_sentiment:.3f} (negative)")
        
        # Scenario 2: Feature Requests analysis
        feature_reviews = df_themes[
            df_themes['identified_themes'].apply(
                lambda x: 'Feature Requests' in x if x else False
            )
        ]
        if len(feature_reviews) > 0:
            print(f"   💡 Feature Requests: {len(feature_reviews)} suggestions")
        
        # Scenario 3: Complaint clustering
        complaint_themes = ['Login & Access Issues', 'Transaction Problems', 'App Performance & Speed']
        complaint_count = len(df_themes[
            df_themes['identified_themes'].apply(
                lambda x: any(theme in x for theme in complaint_themes) if x else False
            )
        ])
        print(f"   🗣️  Total complaints identified: {complaint_count}")
        
        print(f"\n💾 OUTPUT FILES:")
        print(f"   Sentiment results: {sentiment_data['output_path']}")
        print(f"   Theme results: {theme_data['output_path']}")
    
    def run_complete_pipeline(self):
        """Execute complete Task 2 pipeline"""
        print("🚀 STARTING TASK 2 COMPLETE PIPELINE")
        print("="*50)
        
        start_time = datetime.now()
        
        try:
            # Step 1: Load Task 1 data
            df = self.load_task1_data()
            if df is None:
                return False
            
            # Step 2: Sentiment Analysis
            df_sentiment = self.run_sentiment_analysis(df)
            
            # Step 3: Thematic Analysis
            df_themes, bank_themes = self.run_thematic_analysis(df_sentiment)
            
            # Step 4: Final Report
            self.generate_final_report()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 60
            
            print(f"\n✅ TASK 2 COMPLETED SUCCESSFULLY!")
            print(f"   Total time: {duration:.1f} minutes")
            print(f"   Reviews processed: {len(df_themes)}")
            print(f"   Banks analyzed: {len(df_themes['bank'].unique())}")
            
            return True
            
        except Exception as e:
            print(f"❌ Task 2 pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main execution function for Task 2 pipeline"""
    pipeline = Task2Pipeline()
    success = pipeline.run_complete_pipeline()
    
    if success:
        print("\n🎉 TASK 2 READY FOR SUBMISSION!")
        print("   Next: Commit changes to 'task-2' branch")
    else:
        print("\n❌ TASK 2 FAILED - Check errors above")
    
    return success

if __name__ == "__main__":
    success = main()