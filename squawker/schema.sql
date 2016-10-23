-- TODO change this
DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
    id integer PRIMARY KEY autoincrement,
    post_time datetime DEFAULT CURRENT_TIMESTAMP,
    feed varchar(140)
);
