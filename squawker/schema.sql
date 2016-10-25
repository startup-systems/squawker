DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message VARCHAR(140) NOT NULL,
    timestamp INTEGER DEFAULT CURRENT_TIMESTAMP
);
