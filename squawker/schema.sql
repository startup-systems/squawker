-- TODO change this
DROP TABLE IF EXISTS squawkstable;
CREATE TABLE squawkstable (id INTEGER PRIMARY KEY NOT NULL, message varchar(150), timestamp datetime DEFAULT CURRENT_TIMESTAMP);
