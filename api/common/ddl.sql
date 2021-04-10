-- Initialize the database.
-- Drop any existing data and create empty tables.

CREATE SCHEMA IF NOT EXISTS api;

DROP TABLE IF EXISTS people;
CREATE TABLE people (
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  middle_name TEXT,
  last_name TEXT NOT NULL,
  email VARCHAR(255) NOT NULL,
  age INTEGER NOT NULL,
  meta_create_ts DATE,
  meta_update_ts DATE
);