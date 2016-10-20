-- TODO change this
DROP TABLE IF EXISTS mytable;
CREATE TABLE mytable (id INTEGER PRIMARY KEY NOT NULL, content varchar(140), timestamp datetime DEFAULT CURRENT_TIMESTAMP);
