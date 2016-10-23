-- TODO change this
DROP TABLE IF EXISTS squawk_table;

CREATE TABLE squawk_table (
  id INTEGER PRIMARY KEY NOT NULL,
  message varchar(140),
  timestamp datetime DEFAULT CURRENT_TIMESTAMP
);