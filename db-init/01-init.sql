-- Create votes table
CREATE TABLE IF NOT EXISTS votes (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    vote VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_votes_vote ON votes(vote);

-- Insert seed data
INSERT INTO votes (id, vote) VALUES 
    ('seed-1', 'a'),
    ('seed-2', 'b'),
    ('seed-3', 'a'),
    ('seed-4', 'b'),
    ('seed-5', 'a')
ON CONFLICT (id) DO NOTHING;
