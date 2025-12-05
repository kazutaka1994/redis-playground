-- Test data for caching comparison

-- users table (frequently accessed data)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test data (count specified by TEST_USER_COUNT env var, default 1000)
WITH config AS (
    SELECT COALESCE(
        NULLIF(current_setting('app.test_user_count', true), '')::integer,
        1000
    ) AS user_count
)
INSERT INTO users (name, email)
SELECT
    'User' || i,
    'user' || i || '@example.com'
FROM generate_series(1, (SELECT user_count FROM config)) AS i;

-- Indexes for search
CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_users_email ON users(email);
