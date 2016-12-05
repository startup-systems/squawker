-- TODO change this
DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
	id integer PRIMARY KEY, 
	timestamp datetime DEFAULT CURRENT_TIMESTAMP, 
	msg varchar(140)
);
