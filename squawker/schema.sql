-- TODO change this
DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
	id integer primary key autoincrement,
	posts varchar(140),
	timestamp datetime default CURRENT_TIMESTAMP
);
