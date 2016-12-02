-- TODO change this
DROP TABLE IF EXISTS squawker;
CREATE TABLE squawker (id integer primary key autoincrement, message char(140) not null, created_at integer not null);
