/*Initial creation scheme for simple database Creation*/
DROP TABLE IF EXISTS bookList;
CREATE TABLE bookList(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	book_title TEXT NOT NULL,
	book_author TEXT NOT NULL,
	availability TEXT NOT NULL,
	tenant TEXT,
	datedue TEXT
);
