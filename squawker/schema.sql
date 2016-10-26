-- TODO change this
drop table if exists squawks;
create table squawks (
  id integer primary key autoincrement,
  squawk varchar(140),
  time datetime default CURRENT_TIMESTAMP
);