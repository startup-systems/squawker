DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks(
    id integer PRIMARY KEY,
    squawk varchar(140),
    timestamp datetime DEFAULT CURRENT_TIMESTAMP
);
