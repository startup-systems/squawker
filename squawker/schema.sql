-- TODO change this
DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
  id INTEGER PRIMARY KEY,
  squawk VARCHAR(140) DEFAULT NULL,
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
