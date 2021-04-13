-- create users table for auth

CREATE TABLE IF NOT EXISTS api.auth_users
(
    id       SERIAL PRIMARY KEY,
    username TEXT         NOT NULL,
    password VARCHAR(255) NOT NULL
);