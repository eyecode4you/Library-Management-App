"""export_docx_pdf.py - used with library_gui.py to create docx + pdf
	Author: EyeCode4You
	Date: 09/05/2021
"""
from docxtpl import DocxTemplate
from time import time, localtime, asctime
from docx2pdf import convert

def export_to_docx(db_data):
	""" Create docx before pdf for formating """
	db_table = []
	for i in db_data:
		db_table.append({
		'index':i[0],
		'title':i[1],
		'author':i[2],
		'available':i[3],
		#'tenant':i[4],
		#'datedue':i[5]
		})
	date = asctime(localtime(time())) #nice time format
	#import docx template
	template = DocxTemplate('book-list-template.docx')
	#Create template variables
	template_data = {
		'datetime': date,
		'table_contents': db_table
		}
	#render + save book list docx and create pdf
	template.render(template_data)
	template.save('book-list.docx')
	convert('book-list.docx', r'.\\exports') #Create pdf file
