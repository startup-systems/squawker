DROP TABLE IF EXISTS squawktable;
CREATE TABLE squawktable (id integer PRIMARY KEY NOT NULL,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                       squawk char(140)
                      );
