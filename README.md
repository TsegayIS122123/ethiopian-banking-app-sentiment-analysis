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