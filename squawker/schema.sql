
-- TODO change this
DROP TABLE IF EXISTS squawker;
CREATE TABLE squawker (
  id integer primary key,
  squawk varchar(140),
	time datetime CURRENT_TIMESTAMP
	);