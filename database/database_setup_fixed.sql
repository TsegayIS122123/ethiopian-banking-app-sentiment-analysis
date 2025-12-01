-- File: database/database_setup_fixed.sql
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS banks CASCADE;

-- BANKS TABLE remains the same
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_bank_app UNIQUE (bank_name, app_name)
);

-- REVIEWS TABLE with FIXED constraints
CREATE TABLE reviews (
    review_id VARCHAR(20) PRIMARY KEY,
    bank_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(20) NOT NULL CHECK (sentiment_label IN ('POSITIVE', 'NEGATIVE', 'NEUTRAL')),
    sentiment_score NUMERIC(5,4) NOT NULL CHECK (sentiment_score BETWEEN 0 AND 1),
    source VARCHAR(50) DEFAULT 'Google Play',
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE
    -- REMOVED: CONSTRAINT unique_review_per_bank_date UNIQUE (review_text, bank_id, review_date)
);

-- Indexes
CREATE INDEX idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_reviews_date ON reviews(review_date);
CREATE INDEX idx_reviews_sentiment ON reviews(sentiment_label, sentiment_score);

-- Insert banks
INSERT INTO banks (bank_name, app_name) VALUES
('Commercial Bank of Ethiopia', 'Commercial Bank of Ethiopia Mobile'),
('Bank of Abyssinia', 'BoA Mobile'),
('Dashen Bank', 'Dashen Mobile')
ON CONFLICT (bank_name, app_name) DO NOTHING;