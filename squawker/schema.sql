DROP TABLE IF EXISTS tweets;
CREATE TABLE tweets(
    id integer PRIMARY KEY,
    tweet varchar(140),
    timestamp datetime DEFAULT CURRENT_TIMESTAMP,
);
