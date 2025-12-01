-- File: database/verification_queries.sql
-- Verification queries to demonstrate data integrity

-- ============================================================================
-- 1. BASIC DATA COUNTS AND VERIFICATION
-- ============================================================================

-- Total counts (MUST SHOW 3 banks and >1000 reviews)
SELECT 'Banks Count' AS metric, COUNT(*) AS value FROM banks
UNION ALL
SELECT 'Reviews Count', COUNT(*) FROM reviews
UNION ALL
SELECT 'Reviews with Sentiment', COUNT(*) FROM reviews WHERE sentiment_label IS NOT NULL;

-- Reviews per bank with average ratings
SELECT 
    b.bank_name,
    COUNT(r.review_id) AS total_reviews,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    MIN(r.review_date) AS first_review,
    MAX(r.review_date) AS last_review
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_id, b.bank_name
ORDER BY total_reviews DESC;

-- ============================================================================
-- 2. SENTIMENT ANALYSIS VERIFICATION
-- ============================================================================

-- Sentiment distribution per bank
SELECT 
    b.bank_name,
    r.sentiment_label,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY b.bank_name), 2) AS percentage
FROM banks b
JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name, r.sentiment_label
ORDER BY b.bank_name, 
    CASE r.sentiment_label 
        WHEN 'NEGATIVE' THEN 1 
        WHEN 'NEUTRAL' THEN 2 
        WHEN 'POSITIVE' THEN 3 
    END;

-- Average sentiment score by bank and rating
SELECT 
    b.bank_name,
    r.rating,
    COUNT(*) AS review_count,
    ROUND(AVG(r.sentiment_score), 4) AS avg_sentiment_score,
    ROUND(AVG(CASE WHEN r.sentiment_label = 'POSITIVE' THEN 1 ELSE 0 END) * 100, 1) AS positive_pct
FROM banks b
JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name, r.rating
ORDER BY b.bank_name, r.rating DESC;

-- ============================================================================
-- 3. DATA QUALITY CHECKS
-- ============================================================================

-- Missing data check
SELECT 
    'Missing review_text' AS check_type,
    COUNT(*) AS issues
FROM reviews 
WHERE review_text IS NULL OR LENGTH(TRIM(review_text)) = 0
UNION ALL
SELECT 
    'Invalid ratings (not 1-5)',
    COUNT(*)
FROM reviews 
WHERE rating NOT BETWEEN 1 AND 5
UNION ALL
SELECT 
    'Missing sentiment labels',
    COUNT(*)
FROM reviews 
WHERE sentiment_label IS NULL;

-- Duplicate check (should be 0 due to unique constraint)
SELECT 
    'Potential duplicates' AS check_type,
    COUNT(*) - COUNT(DISTINCT (review_text, bank_id, review_date)) AS issues
FROM reviews;

-- ============================================================================
-- 4. TEMPORAL ANALYSIS
-- ============================================================================

-- Monthly review trends
SELECT 
    b.bank_name,
    DATE_TRUNC('month', r.review_date) AS review_month,
    COUNT(*) AS reviews_count,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    ROUND(AVG(CASE WHEN r.sentiment_label = 'POSITIVE' THEN 1 ELSE 0 END) * 100, 1) AS positive_pct
FROM banks b
JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name, DATE_TRUNC('month', r.review_date)
ORDER BY b.bank_name, review_month DESC
LIMIT 12;  -- Last 12 months

-- ============================================================================
-- 5. TOP COMPLAINTS BY THEME (Using keywords from Task 2)
-- ============================================================================

-- Top negative reviews by bank (for manual inspection)
SELECT 
    b.bank_name,
    r.rating,
    r.review_text,
    r.sentiment_score,
    LEFT(r.review_text, 100) AS preview
FROM banks b
JOIN reviews r ON b.bank_id = r.bank_id
WHERE r.sentiment_label = 'NEGATIVE'
    AND r.rating IN (1, 2)
ORDER BY r.sentiment_score DESC, r.review_date DESC
LIMIT 10;