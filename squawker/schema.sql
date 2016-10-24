
DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
  id integer primary key autoincrement,
  phrase varchar(140) NOT NULL ,
  time datetime NOT NULL
);
