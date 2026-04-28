-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    username    VARCHAR(50) UNIQUE NOT NULL,
    email       VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Games Table
CREATE TABLE IF NOT EXISTS games (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scores Table
CREATE TABLE IF NOT EXISTS scores (
    id           SERIAL PRIMARY KEY,
    user_id      INTEGER REFERENCES users(id) ON DELETE CASCADE,
    game_id      INTEGER REFERENCES games(id) ON DELETE CASCADE,
    score        FLOAT NOT NULL,
    submitted_at TIMESTAMP DEFAULT NOW()
);