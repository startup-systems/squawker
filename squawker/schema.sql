-- TODO change this
DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  squawk CHAR(140) NOT NULL;
  time datetime default CURRENT_TIMESTAMP
  );
