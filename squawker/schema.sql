-- -- TODO change this
-- DROP TABLE IF EXISTS mytable;
-- CREATE TABLE mytable (id integer);

DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
  id integer primary key autoincrement,
  squawk varchar(141) not null
);
