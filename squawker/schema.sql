DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
    id integer primary key autoincrement,
    text text not null, 
    timestamp datetime DEFAULT CURRENT_TIMESTAMP);
