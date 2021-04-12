-- Initialize the database.

CREATE TABLE IF NOT EXISTS api.person
(
    id             SERIAL PRIMARY KEY,
    first_name     TEXT         NOT NULL,
    middle_name    TEXT,
    last_name      TEXT         NOT NULL,
    email          VARCHAR(255) NOT NULL,
    age            INTEGER      NOT NULL,
    meta_create_ts timestamptz
);