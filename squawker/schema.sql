-- TODO change this
DROP TABLE IF EXISTS mytable;
CREATE TABLE squawks (
	id integer primary key autoincrement,
	squawk varchar(140),
	time_stamp datetime default CURRENT_TIMESTAMP
);
