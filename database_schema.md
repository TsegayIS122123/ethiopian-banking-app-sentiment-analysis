-- PostgreSQL Database Schema for Bank Reviews

Table: banks
Columns:
  - bank_id (integer) NOT NULL
  - bank_name (character varying) NOT NULL
  - app_name (character varying) NOT NULL
  - created_at (timestamp without time zone) NULL

Table: reviews
Columns:
  - review_id (character varying) NOT NULL
  - bank_id (integer) NULL
  - review_text (text) NOT NULL
  - rating (integer) NULL
  - review_date (date) NOT NULL
  - sentiment_label (character varying) NULL
  - sentiment_score (numeric) NULL
  - source (character varying) NULL
  - created_at (timestamp without time zone) NULL

