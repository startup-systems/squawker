-- TODO change this
DROP TABLE IF EXISTS squawks;
CREATE TABLE squawks (
	id integer primary key autoincrement,
	title text not null,
	'text' text not null
    CHECK(
        length("text") <= 140
    )
);
