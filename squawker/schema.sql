-- TODO change this
DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	time REAL,
	username TEXT,
	text TEXT
);
