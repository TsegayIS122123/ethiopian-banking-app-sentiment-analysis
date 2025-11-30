# 🏦 Ethiopian Banking App Analytics

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

A data-driven analysis of customer experience for Ethiopian banking mobile applications using Google Play Store reviews. This project leverages NLP and sentiment analysis to provide actionable insights for product improvement.

## 📊 Business Context

**Omega Consultancy** is assisting three major Ethiopian banks in enhancing their mobile banking applications:
- 🏦 **Commercial Bank of Ethiopia (CBE)**
- 🏦 **Bank of Abyssinia (BOA)** 
- 🏦 **Dashen Bank**

This analysis addresses critical business questions around user retention, feature enhancement, and complaint management.

## 🎯 Project Objectives

- **Scrape & Analyze** 1,200+ user reviews from Google Play Store
- **Quantify Sentiment** using DistilBERT model for precise emotion detection
- **Identify Key Themes** in customer feedback through NLP techniques
- **Provide Data-Driven Recommendations** for app improvement
- **Build PostgreSQL Database** for structured data storage

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| **Data Collection** | `google-play-scraper` |
| **Data Processing** | `pandas`, `numpy` |
| **NLP & Analysis** | `transformers`, `torch`, `nltk` |
| **Visualization** | `matplotlib`, `seaborn`, `wordcloud` |
| **Database** | `PostgreSQL`, `psycopg2` |
| **Environment** | `python-dotenv` |

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/TsegayIS122123/ethiopian-banking-app-sentiment-analysis.git
   cd ethiopian-banking-app-sentiment-analysis
# Set up virtual environment

- python -m venv .venv
- .venv\Scripts\activate   

# install dependencies

pip install -r requirements.txt


## Task 1: Data Collection & Preprocessing 

### 📊 Results Summary
- **Total Reviews Collected**: 1,350 raw → 1,244 clean reviews
- **Reviews per Bank**: 414-415 reviews per bank (Target: 400+ )
- **Data Quality**: 0.00% missing data (Target: <5% )
- **Data Retention**: 92.1% of original data preserved

### 🎯 KPIs Achieved
-  1,200+ reviews collected (1,244 total)
-  <5% missing data (0.00%)
-  Clean CSV dataset created
-  Organized Git repository with clear commits
-  400+ reviews per bank achieved

### 📋 Methodology

#### Data Collection
- Used `google-play-scraper` Python library with OOP approach
- Targeted three Ethiopian banking apps:
  - Commercial Bank of Ethiopia (CBE)
  - Bank of Abyssinia (BOA) 
  - Dashen Bank
- Collected **450 reviews per bank** to ensure 400+ after cleaning
- **Retry mechanism** with exponential backoff for reliability
- Data includes: review text, rating (1-5), date, user name, bank name, app version

#### Data Preprocessing Pipeline
1. **Duplicate Removal**: Removed reviews with identical content, user, and date
2. **Missing Data Handling**: 
   - Removed reviews with empty text
   - Filled missing user names with 'Anonymous'
   - Filled missing thumbs-up counts with 0
3. **Language Filtering**: 
   - Removed Amharic-only content (106 reviews filtered)
   - Removed garbage text, emoji-only, and very short reviews
   - Preserved mixed-language reviews with banking keywords
4. **Date Normalization**: Converted all dates to YYYY-MM-DD format
5. **Text Cleaning**: Standardized whitespace and preserved meaningful content
6. **Column Standardization**: Selected only required columns (review, rating, date, bank, source)


### 📈 Data Insights
- **Rating Distribution**: 60.0% positive (4-5⭐), 21.6% negative (1⭐)
- **Date Range**: November 2022 to November 2025
- **Text Characteristics**: Average review length 52.7 characters
- **Bank Performance**: All banks achieved target review counts

### 🚀 Next Steps
Ready for **Task 2**: Sentiment Analysis & Thematic Analysis
- Perform sentiment analysis on cleaned reviews
- Extract key themes and pain points per bank
- Generate actionable recommendations for each bank
### Task 2: Sentiment & Thematic Analysis

#### Sentiment Analysis
- **Model**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Architecture**:
  - Transformer-based model fine-tuned on SST-2 dataset
  - Binary classification (Positive/Negative) with confidence scores
- **Processing**:
  - Batch processing (32 reviews/batch) for efficiency
  - GPU acceleration support with CPU fallback
  - Neutral classification threshold (0.4-0.6 confidence range)
- **Output**:
  - `sentiment_label`: POSITIVE/NEGATIVE/NEUTRAL
  - `sentiment_score`: Confidence score (0-1)
  - `sentiment_numeric`: Numerical scale (-1 to +1) for aggregation

#### Thematic Analysis
- **Keyword Extraction**: TF-IDF (Term Frequency-Inverse Document Frequency)
  - N-gram range: 1-3 (unigrams, bigrams, trigrams)
  - Maximum features: 100 most significant terms
  - Stop word removal and minimum document frequency
- **Theme Clustering**: Rule-based approach
  - 8 predefined banking-specific theme categories
  - Pattern matching on cleaned review text
  - Multi-keyword matching per theme
- **Theme Categories**:
  1. Login & Access Issues
  2. Transaction Problems
  3. App Performance & Speed
  4. User Interface & Experience
  5. Customer Support
  6. Security Concerns
  7. Feature Requests
  8. Network & Connectivity

#### Analysis Pipeline
- Raw Reviews → Text Cleaning → Sentiment Analysis → Thematic Analysis → Insights
## 🗄️ Database Implementation (Task 3)

### PostgreSQL Database Schema

#### Banks Table
- `bank_id` (SERIAL PRIMARY KEY) - Auto-incrementing unique identifier
- `bank_name` (VARCHAR(100)) - Full bank name
- `app_name` (VARCHAR(200)) - Mobile application name
- `created_at` (TIMESTAMP) - Record creation timestamp

#### Reviews Table
- `review_id` (VARCHAR(50) PRIMARY KEY) - Unique review identifier
- `bank_id` (INTEGER FOREIGN KEY) - Reference to banks table
- `review_text` (TEXT) - The actual review content
- `rating` (INTEGER CHECK 1-5) - Star rating (1-5)
- `review_date` (DATE) - Date of review
- `sentiment_label` (VARCHAR(10)) - POSITIVE/NEGATIVE/NEUTRAL
- `sentiment_score` (DECIMAL(3,2)) - Sentiment confidence score (0-1)
- `source` (VARCHAR(50)) - Data source (Google Play)
- `created_at` (TIMESTAMP) - Record creation timestamp

### Database Statistics
- **Total Reviews**: 1,244 reviews stored
- **Banks Coverage**: 3 Ethiopian banks
- **Data Integrity**: Full referential integrity maintained
- **Performance**: Batch insertion with error handling

### Key SQL Queries
```sql
-- Reviews per bank
SELECT b.bank_name, COUNT(*) as review_count 
FROM banks b JOIN reviews r ON b.bank_id = r.bank_id 
GROUP BY b.bank_name;

-- Average rating per bank
SELECT b.bank_name, ROUND(AVG(r.rating), 2) as avg_rating
FROM banks b JOIN reviews r ON b.bank_id = r.bank_id 
GROUP BY b.bank_name;

-- Sentiment distribution
SELECT sentiment_label, COUNT(*) as count 
FROM reviews 
GROUP BY sentiment_label;