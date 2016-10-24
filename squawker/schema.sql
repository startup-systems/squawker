-- TODO change this
DROP TABLE IF EXISTS mytable;
CREATE TABLE squawks (
	id integer primary key,
	squawk varchar(140),
	time datetime CURRENT_TIMESTAMP
	);
