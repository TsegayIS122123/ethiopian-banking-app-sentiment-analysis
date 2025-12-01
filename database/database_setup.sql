-- Enhanced with explicit constraints and documentation
-- File: database/database_setup.sql

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS banks CASCADE;

-- ============================================================================
-- 1. BANKS TABLE - Master table for bank information
-- ============================================================================
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Business rule: Unique combination of bank and app name
    CONSTRAINT unique_bank_app UNIQUE (bank_name, app_name)
);

COMMENT ON TABLE banks IS 'Master table containing bank and app information';
COMMENT ON COLUMN banks.bank_id IS 'Primary key, auto-incrementing ID';
COMMENT ON COLUMN banks.bank_name IS 'Full name of the bank (e.g., Commercial Bank of Ethiopia)';
COMMENT ON COLUMN banks.app_name IS 'Name of the mobile banking app';

-- ============================================================================
-- 2. REVIEWS TABLE - Stores processed review data from Task 2
-- ============================================================================
CREATE TABLE reviews (
    review_id VARCHAR(20) PRIMARY KEY, -- e.g., REVIEW_0001
    bank_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(20) NOT NULL CHECK (sentiment_label IN ('POSITIVE', 'NEGATIVE', 'NEUTRAL')),
    sentiment_score NUMERIC(5,4) NOT NULL CHECK (sentiment_score BETWEEN 0 AND 1),
    source VARCHAR(50) DEFAULT 'Google Play',
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key relationship
    FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE,
    
    -- Business rule: Prevent exact duplicate reviews for same bank on same day
    CONSTRAINT unique_review_per_bank_date UNIQUE (review_text, bank_id, review_date)
);

COMMENT ON TABLE reviews IS 'Stores processed review data including sentiment analysis results';
COMMENT ON COLUMN reviews.review_id IS 'Primary key, unique review identifier from Task 2';
COMMENT ON COLUMN reviews.sentiment_score IS 'Sentiment confidence score from DistilBERT model';
COMMENT ON COLUMN reviews.sentiment_label IS 'Categorical sentiment (POSITIVE/NEGATIVE/NEUTRAL)';

-- ============================================================================
-- 3. INDEXES FOR PERFORMANCE
-- ============================================================================
CREATE INDEX idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_reviews_date ON reviews(review_date);
CREATE INDEX idx_reviews_sentiment ON reviews(sentiment_label, sentiment_score);
CREATE INDEX idx_reviews_sentiment_score ON reviews(sentiment_score DESC);

-- ============================================================================
-- 4. SAMPLE DATA INSERTION (for verification)
-- ============================================================================
-- Insert bank data
INSERT INTO banks (bank_name, app_name) VALUES
('Commercial Bank of Ethiopia', 'Commercial Bank of Ethiopia Mobile'),
('Bank of Abyssinia', 'BoA Mobile'),
('Dashen Bank', 'Dashen Mobile');

-- Note: The actual review data will be inserted via Python script