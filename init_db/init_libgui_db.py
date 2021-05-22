"""	init_libgui_db.py - Use schema.sql to create initial library db
	Create a simple database to use with FFIreland Library app"""
import sqlite3

connection = sqlite3.connect('library.db')
with open('schema.sql') as f:
	"""Open our created sql schema & execute for initial db structure"""
	connection.executescript(f.read())

cur = connection.cursor()
with open("book_data.txt", "r") as f: #open and parse books to db
	booklist = f.read().split(';')
	for i in booklist:
		i = i.strip() #Remove \n etc...
		bookdata = i.split('-')
		try: #Last line in txt file causes out of list index, continue
			cur.execute("INSERT INTO bookList (book_title, book_author, availability, tenant, datedue) VALUES (?, ?, ?, ?, ?)",
						(bookdata[0], bookdata[1], 'yes', None, None))
		except:
			continue		
connection.commit() #apply changes
connection.close() #end connection
print("Database Successfully Created!")
