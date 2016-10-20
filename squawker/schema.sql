-- TODO change this
-- DROP TABLE IF EXISTS mytable;
-- CREATE TABLE mytable (id integer);
drop table if exists entries;
create table entries (
      id integer primary key autoincrement,
      title text not null,
      'text' text not null
);
