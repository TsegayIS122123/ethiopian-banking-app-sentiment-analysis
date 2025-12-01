-- Database Dump for Bank Reviews Project
-- Generated: 2025-12-01 21:37:14
-- Total reviews: 1244

-- Schema:

-- banks table structure:
-- Columns: 4
--   bank_id: integer (not null)
--   bank_name: character varying (not null)
--   app_name: character varying (not null)
--   created_at: timestamp without time zone (nullable)

-- reviews table structure:
-- Columns: 9
--   review_id: character varying (not null)
--   bank_id: integer (not null)
--   review_text: text (not null)
--   rating: integer (not null)
--   review_date: date (not null)
--   sentiment_label: character varying (not null)
--   sentiment_score: numeric (not null)
--   source: character varying (nullable)
--   processed_at: timestamp without time zone (nullable)
