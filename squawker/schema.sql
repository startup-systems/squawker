-- TODO change this
DROP TABLE IF EXISTS mytable;
CREATE TABLE mytable (id integer);
DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
	id integer primary key autoincrement,
	squawks varchar(140) not NULL,
	time datetime CURRENT_TIMESTAMP,
	);


