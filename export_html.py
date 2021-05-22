"""	export_html.py - Export database data to html file
	Author: EyeCode4You
	Date: 22/05/2021
"""
from jinja2 import Environment, FileSystemLoader
from time import time, localtime, asctime

def export_to_html(db_data):
	env = Environment(loader=FileSystemLoader('.'))
	template = env.get_template('template.html')
	
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
	template = env.get_template('template.html')
	template_data = {
		'datetime': date,
		'table_contents': db_table
		}
	html_out = template.render(template_data)
	with open('./exports/book-list.html', 'w') as f: #write data to html file
		f.write(html_out)
	
