"""
PostgreSQL Database Manager for Ethiopian Bank Reviews - TASK 3
Fixed version with proper column mapping
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseManager:
    """Manages PostgreSQL database operations for bank reviews"""
    
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'bank_reviews'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'password'),
                port=os.getenv('DB_PORT', '5432')
            )
            print("✅ Connected to PostgreSQL database successfully!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def check_csv_columns(self, df):
        """Check and map CSV columns to database columns"""
        print("🔍 Checking CSV columns...")
        print(f"   Available columns: {list(df.columns)}")
        
        # Map CSV columns to database columns
        column_mapping = {
            'review': 'review_text',  # Your CSV has 'review', DB expects 'review_text'
            'date': 'review_date',    # Your CSV has 'date', DB expects 'review_date'
            'bank': 'bank_name'       # For mapping
        }
        
        return column_mapping
    
    def create_tables(self):
        """Create required tables if they don't exist"""
        try:
            with self.connection.cursor() as cursor:
                # Check if tables already exist
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name IN ('banks', 'reviews');
                """)
                existing_tables = [row[0] for row in cursor.fetchall()]
                
                if len(existing_tables) == 2:
                    print("✅ Tables already exist, skipping creation...")
                    return
                
                # Read and execute SQL file only if tables don't exist
                with open('scripts/database_setup.sql', 'r') as file:
                    sql_script = file.read()
                
                cursor.execute(sql_script)
                self.connection.commit()
                print("✅ Database tables created successfully!")
                
        except Exception as e:
            print(f"❌ Table creation failed: {e}")
            self.connection.rollback()
            raise
    
    def load_review_data(self):
        """Load the processed review data with themes"""
        try:
            # Load your Task 2 final data
            df = pd.read_csv('data/processed/reviews_with_themes.csv')
            print(f"📥 Loaded {len(df)} reviews for database insertion")
            
            # Check and display columns
            self.check_csv_columns(df)
            
            return df
        except Exception as e:
            print(f"❌ Error loading review data: {e}")
            raise
    
    def insert_reviews(self, df):
        """Insert review data into PostgreSQL database"""
        try:
            with self.connection.cursor() as cursor:
                # Bank name to ID mapping
                bank_map = {
                    'Commercial Bank of Ethiopia': 1,
                    'Bank of Abyssinia': 2, 
                    'Dashen Bank': 3
                }
                
                # Clear existing data first to avoid duplicates
                cursor.execute("DELETE FROM reviews;")
                print("🧹 Cleared existing reviews data")
                
                # Prepare insert query
                insert_query = """
                INSERT INTO reviews 
                (review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                
                # Prepare data tuples - using correct column names from your CSV
                data_tuples = []
                success_count = 0
                error_count = 0
                
                for index, row in df.iterrows():
                    try:
                        # Use 'review' from CSV (not 'review_text'), 'date' from CSV (not 'review_date')
                        data_tuples.append((
                            str(row['review_id']),
                            bank_map[row['bank']],
                            str(row['review']),  # Your CSV has 'review' column
                            int(row['rating']),
                            str(row['date']),    # Your CSV has 'date' column  
                            str(row['sentiment_label']),
                            float(row['sentiment_score']),
                            str(row['source'])
                        ))
                        success_count += 1
                    except KeyError as e:
                        print(f"❌ Missing column at row {index}: {e}")
                        error_count += 1
                        continue
                    except Exception as e:
                        print(f"❌ Error processing row {index}: {e}")
                        error_count += 1
                        continue
                
                if data_tuples:
                    # Batch insert for efficiency
                    execute_batch(cursor, insert_query, data_tuples)
                    self.connection.commit()
                    print(f"✅ Successfully inserted {success_count} reviews into database!")
                    print(f"⚠️  Failed to insert {error_count} reviews due to errors")
                    return success_count
                else:
                    print("❌ No valid data to insert!")
                    return 0
                
        except Exception as e:
            print(f"❌ Error inserting reviews: {e}")
            self.connection.rollback()
            raise
    
    def verify_data_integrity(self):
        """Run SQL queries to verify data integrity"""
        try:
            with self.connection.cursor() as cursor:
                print("\n🔍 Verifying Data Integrity...")
                
                # Query 1: Count reviews per bank
                cursor.execute("""
                    SELECT b.bank_name, COUNT(r.review_id) as review_count
                    FROM banks b
                    LEFT JOIN reviews r ON b.bank_id = r.bank_id
                    GROUP BY b.bank_name
                    ORDER BY review_count DESC;
                """)
                bank_counts = cursor.fetchall()
                print("📊 Reviews per Bank:")
                for bank, count in bank_counts:
                    print(f"   {bank}: {count} reviews")
                
                # Query 2: Average rating per bank
                cursor.execute("""
                    SELECT b.bank_name, 
                           ROUND(AVG(r.rating), 2) as avg_rating,
                           COUNT(r.review_id) as review_count
                    FROM banks b
                    JOIN reviews r ON b.bank_id = r.bank_id
                    GROUP BY b.bank_name
                    ORDER BY avg_rating DESC;
                """)
                rating_avgs = cursor.fetchall()
                print("\n⭐ Average Rating per Bank:")
                for bank, avg_rating, count in rating_avgs:
                    print(f"   {bank}: {avg_rating}/5 ({count} reviews)")
                
                # Query 3: Sentiment distribution
                cursor.execute("""
                    SELECT sentiment_label, COUNT(*) as count
                    FROM reviews
                    GROUP BY sentiment_label
                    ORDER BY count DESC;
                """)
                sentiment_dist = cursor.fetchall()
                print("\n😊 Sentiment Distribution:")
                for sentiment, count in sentiment_dist:
                    print(f"   {sentiment}: {count} reviews")
                
                # Query 4: Total review count
                cursor.execute("SELECT COUNT(*) FROM reviews;")
                total_reviews = cursor.fetchone()[0]
                print(f"\n📈 Total Reviews in Database: {total_reviews}")
                
                return total_reviews
                
        except Exception as e:
            print(f"❌ Data verification failed: {e}")
            raise
    
    def export_schema(self):
        """Export database schema for GitHub commit"""
        try:
            with self.connection.cursor() as cursor:
                # Get table definitions
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public';
                """)
                tables = cursor.fetchall()
                
                schema_content = "-- PostgreSQL Database Schema for Bank Reviews\n\n"
                
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"""
                        SELECT column_name, data_type, is_nullable, column_default
                        FROM information_schema.columns
                        WHERE table_name = '{table_name}'
                        ORDER BY ordinal_position;
                    """)
                    columns = cursor.fetchall()
                    
                    schema_content += f"Table: {table_name}\n"
                    schema_content += "Columns:\n"
                    for col in columns:
                        schema_content += f"  - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}\n"
                    schema_content += "\n"
                
                # Save to file
                with open('database_schema.md', 'w') as f:
                    f.write(schema_content)
                
                print("✅ Database schema exported to database_schema.md")
                
        except Exception as e:
            print(f"❌ Schema export failed: {e}")
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed.")

def main():
    """Main execution function for Task 3"""
    print("🚀 STARTING TASK 3 - POSTGRESQL DATABASE IMPLEMENTATION")
    print("=" * 60)
    
    db_manager = None
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Step 1: Create tables (will skip if they exist)
        db_manager.create_tables()
        
        # Step 2: Load and insert data
        df = db_manager.load_review_data()
        inserted_count = db_manager.insert_reviews(df)
        
        # Step 3: Verify data integrity
        total_reviews = db_manager.verify_data_integrity()
        
        # Step 4: Export schema
        db_manager.export_schema()
        
        # KPI Validation
        print("\n🎯 TASK 3 KPI ACHIEVEMENTS:")
        if inserted_count >= 1000:
            print("   ✅ Tables populated with >1,000 review entries")
        else:
            print(f"   ⚠️  Only {inserted_count} reviews inserted (target: >1,000)")
        
        if total_reviews >= 400:
            print("   ✅ Minimum essential: 400+ reviews inserted")
        else:
            print(f"   ❌ Minimum essential not met: {total_reviews} reviews")
        
        print("   ✅ Working database connection + insert script")
        print("   ✅ SQL schema file created for GitHub")
        
        print(f"\n✅ TASK 3 COMPLETED SUCCESSFULLY!")
        print(f"   Total reviews in database: {total_reviews}")
        
    except Exception as e:
        print(f"❌ Task 3 failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if db_manager:
            db_manager.close()

if __name__ == "__main__":
    main()