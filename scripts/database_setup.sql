-- Create banks table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create reviews table  
CREATE TABLE reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(10),
    sentiment_score DECIMAL(3,2),
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert bank data
INSERT INTO banks (bank_name, app_name) VALUES
('Commercial Bank of Ethiopia', 'Commercial Bank of Ethiopia Mobile'),
('Bank of Abyssinia', 'Bank of Abyssinia Mobile Banking'), 
('Dashen Bank', 'Dashen Bank Mobile Banking');