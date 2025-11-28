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
- PostgreSQL (optional for Task 3)
- Git

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/TsegayIS122123/ethiopian-banking-app-sentiment-analysis.git
   cd ethiopian-banking-app-sentiment-analysis
# Set up virtual environment

python -m venv .venv
.venv\Scripts\activate   

# install dependencies

pip install -r requirements.txt
