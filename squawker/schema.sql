-- TODO change this
DROP TABLE IF EXISTS mytable;
CREATE TABLE mytable (
	id integer primary key autoincrement,
	phrase varchar(140) NOT NULL,
	time datetime NOT NULL
);
