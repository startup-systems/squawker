-- TODO change this
DROP TABLE IF EXISTS squawker;
CREATE TABLE squawker (id integer primary key autoincrement,squawks varchar(140) not NULL,time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

