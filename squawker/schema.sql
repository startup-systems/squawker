-- TODO change this
DROP TABLE IF EXISTS squawks;
-- CREATE TABLE mytable (id integer);
-- CREATE TABLE squawks (id INT, body text);
CREATE TABLE squawks (id INTEGER PRIMARY KEY AUTOINCREMENT, body TEXT);
INSERT INTO squawks(body) VALUES ("This is the test entry from db");
INSERT INTO squawks(body) VALUES ("Another one");
