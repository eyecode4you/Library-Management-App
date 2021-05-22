""" library_gui.py
	Forest Friends Ireland Library Management System
	Author: EyeCode4You
	Date: 09/05/2021
	Version: 1.6
"""
#Imports: tkinter - GUI, sqlite3 - Database
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, export_docx_pdf, export_html

def update(rows):
	""" Display rows in app from db """
	trv.delete(*trv.get_children())
	for i in rows:
		trv.insert('', 'end', values=i)

#Wrapper 2 button functions	
def search():
	""" Allow searching by book title """
	q2 = q.get()
	query = "SELECT id, book_title, book_author, availability, tenant, datedue FROM bookList WHERE book_title LIKE '%"+q2+"%'"
	cursor.execute(query)
	rows = cursor.fetchall()
	update(rows)

def clear():
	""" Reset app row view to initial """
	q.set('') #Clear search input
	query = "SELECT id, book_title, book_author, availability, tenant, datedue FROM bookList"
	cursor.execute(query)
	rows = cursor.fetchall()
	update(rows)

def export():
	""" Export db data to pdf file """
	query = "SELECT id, book_title, book_author, availability, tenant, datedue FROM bookList"
	cursor.execute(query)
	db_data = cursor.fetchall()
	export_docx_pdf.export_to_docx(db_data)
	messagebox.showinfo("Note", "File exported as: book-list.pdf")
	
def export2():
	""" Export db data to html file """
	query = "SELECT id, book_title, book_author, availability, tenant, datedue FROM bookList"
	cursor.execute(query)
	db_data = cursor.fetchall()
	export_html.export_to_html(db_data)
	messagebox.showinfo("Note", "File exported as: book-list.html")

#Wrapper 3 button functions
def update_bookdata():
	""" Update currently selected book data entry """
	bId = t0.get()
	btitle = t1.get()
	bauthor = t2.get()
	bavailable = t3.get()
	btenant = t4.get()
	bdatedue = t5.get()
	
	if messagebox.askyesno("Warning!", "Are you sure you want to update this entry?"):
		if '' in {btitle, bauthor, bavailable}:
			messagebox.showerror("ERROR!", "Please ensure at least Title, Author, and Availability fields are filled!")
		else:
			query = "UPDATE bookList SET book_title = ?, book_author = ?, availability = ?, tenant = ?, datedue = ? WHERE id = ?"
			cursor.execute(query, (btitle, bauthor, bavailable, btenant, bdatedue, bId))
			clear()
	else:
		return True

def add_new_book():
	""" Add new bookdata entry """
	btitle = t1.get()
	bauthor = t2.get()
	bavailable = t3.get()
	btenant = t4.get()
	bdatedue = t5.get()
	query = "INSERT INTO bookList(id, book_title, book_author, availability, tenant, datedue) VALUES(?, ?, ?, ?, ?, ?)"
	if '' in {btitle, bauthor, bavailable}: #Check all fields are filled
		messagebox.showerror("ERROR!", "Please ensure at least Title, Author, and Availability fields are filled! (ID not required)")
	else:
		cursor.execute(query, (None, btitle, bauthor, bavailable, btenant, bdatedue))
		clear()

def delete_bookdata():
	""" Delete bookdata entry """
	book_id = t0.get()
	if messagebox.askyesno("Confirm Deletion?", "Are you sure you want to delete this book data?"):
		try:
			query = "DELETE FROM bookList WHERE id = "+book_id
			cursor.execute(query)
			clear()
		except sqlite3.OperationalError as e:
			messagebox.showerror('Error in ID Selection!', str(e) + ' (Ensure you have the correct book ID inserted!)')
	else:
		return True
		
def clearWrap3Fields():
	""" Clear all wrapper 3 input data """
	e = ''
	t0.set(e)
	t1.set(e)
	t2.set(e)
	t3.set(e)
	t4.set(e)
	t5.set(e)

def save_db_changes():
	""" Commit changes to library database """
	if messagebox.askyesno("Warning!", "Are you sure you want to commit changes? This cannot be undone!"):
		conn.commit() #Save changes to database
	else:
		return True

def getrow(event):
	""" Populate wrapper 3 entries with data """
	rowid = trv.identify_row(event.y)
	item = trv.item(trv.focus())
	t0.set(item['values'][0])
	t1.set(item['values'][1])
	t2.set(item['values'][2])
	t3.set(item['values'][3])
	t4.set(item['values'][4])
	t5.set(item['values'][5])

#START - Setup
conn = sqlite3.connect('library.db')
cursor = conn.cursor() #create database cursor object
cursor.execute('SELECT * FROM bookList')
root = Tk()

wrapper1 = LabelFrame(root, text='Book List')
wrapper2 = LabelFrame(root, text='Options')
wrapper3 = LabelFrame(root, text='Book Data')
wrapper1.pack(fill='both', expand='no', padx=20, pady=10)
wrapper2.pack(fill='both', expand='no', padx=20, pady=1)
wrapper3.pack(fill='both', expand='yes', padx=20, pady=10)

"""***BOOK-LIST-WRAPPER1-SECTION***"""
trv = ttk.Treeview(wrapper1, columns=(1,2,3,4,5,6), show='headings', height='14')
trv.pack(side=LEFT)

#TRV Headings
trv.heading(1, text='ID')
trv.heading(2, text='BookTitle')
trv.heading(3, text='BookAuthor')
trv.heading(4, text='Availablity')
trv.heading(5, text='Tenant(MemberID)')
trv.heading(6, text='DateDue')

trv.bind('<Double 1>', getrow) #When double clicking entry getrow()

#Vertical Scrollbar
yscrollbar = ttk.Scrollbar(wrapper1, orient='vertical', command=trv.yview)
yscrollbar.pack(side=RIGHT, fill='y')
trv.configure(yscrollcommand=yscrollbar.set)

#Pop. Book List Wrapper
query = "SELECT id, book_title, book_author, availability, tenant, datedue FROM bookList"
cursor.execute(query)
rows = cursor.fetchall()
update(rows)

"""***OPTIONS-WRAPPER2-SECTION***"""
#Search functionality
q = StringVar() #Search Term
lbl = Label(wrapper2, text='Search:')
lbl.pack(side=tk.LEFT, padx=10, pady=20)
ent = Entry(wrapper2, textvariable=q)
ent.pack(side=tk.LEFT, padx=6)
btn = Button(wrapper2, text='Search', command=search)
btn.pack(side=tk.LEFT, padx=6)
clrbtn = Button(wrapper2, text='Clear', command=clear)
clrbtn.pack(side=tk.LEFT, padx=6)

#export as pdf
lbl = Label(wrapper2, text='Options:')
lbl.pack(side=tk.LEFT, padx=10)
expbtn = Button(wrapper2, text='Export as PDF\n(Microsoft Word Required)', command=export)
expbtn.pack(side=tk.LEFT, padx=6)

expbtn = Button(wrapper2, text='Export as HTML', command=export2)
expbtn.pack(side=tk.LEFT, padx=6)

"""***BOOKDATA-WRAPPER3-SECTION***"""
t0, t1, t2, t3, t4, t5 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
lbl0 = Label(wrapper3, text='Book ID:')
lbl0.grid(row=0, column=0, padx=5, pady=5)
ent1 = Entry(wrapper3, textvariable=t0)
ent1.grid(row=0, column=1, padx=5, pady=5)
lbl1 = Label(wrapper3, text='Book Title:')
lbl1.grid(row=1, column=0, padx=5, pady=5)
ent1 = Entry(wrapper3, textvariable=t1)
ent1.grid(row=1, column=1, padx=5, pady=5)
lbl2 = Label(wrapper3, text='Book Author:')
lbl2.grid(row=2, column=0, padx=5, pady=5)
ent2 = Entry(wrapper3, textvariable=t2)
ent2.grid(row=2, column=1, padx=5, pady=5)
lbl3 = Label(wrapper3, text='Availability:')
lbl3.grid(row=3, column=0, padx=5, pady=5)
ent3 = Entry(wrapper3, textvariable=t3)
ent3.grid(row=3, column=1, padx=5, pady=5)
lbl4 = Label(wrapper3, text='Tenant:')
lbl4.grid(row=4, column=0, padx=5, pady=5)
ent4 = Entry(wrapper3, textvariable=t4)
ent4.grid(row=4, column=1, padx=5, pady=5)
lbl5 = Label(wrapper3, text='DateDue:')
lbl5.grid(row=5, column=0, padx=5, pady=6)
ent5 = Entry(wrapper3, textvariable=t5)
ent5.grid(row=5, column=1, padx=5, pady=6)

clr_btn = Button(wrapper3, text='Clear All', command=clearWrap3Fields) #Clear all input fields
clr_btn.grid(row=5, column=2, padx=5, pady=5)

upd_btn = Button(wrapper3, text='Update', command=update_bookdata)
add_btn = Button(wrapper3, text='Add New', command=add_new_book)
del_btn = Button(wrapper3, text='Delete', command=delete_bookdata)
sav_btn = Button(wrapper3, text='Save Changes', command=save_db_changes)
upd_btn.grid(row=6, column=0, padx=5, pady=3)
add_btn.grid(row=6, column=1, padx=5, pady=3)
del_btn.grid(row=6, column=2, padx=5, pady=3)
sav_btn.grid(row=6, column=3, padx=5, pady=3)

#tkinter window setup and run
root.title('FFIreland Library System')
root.geometry('1280x725')
root.mainloop()
