-- TODO change this
DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  squawk VARCHAR(140),
  time_stamp DATETIME
);