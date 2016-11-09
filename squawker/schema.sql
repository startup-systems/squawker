-- TODO change this
DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
	id integer primary key autoincrement,
	squawk varchar(140) NOT NULL
);