import sqlite3

silent_prints = 0
import re

def db_execute(database, expression, silent = False):
	global silent_prints
	if not silent:
		print(re.sub('\s+', ' ', expression))
	else:
		silent_prints += 1
		if silent_prints % 50 == 0:
			print('.', end = ('' if silent_prints % 500 != 0 else '\n'))
	connection = sqlite3.connect(database)
	cursorObj = connection.cursor()

	try:
		cursorObj.execute(expression)
	except sqlite3.IntegrityError:
		print('Database execution failed, uniqueness of Primary Keys has been violated >:(')
	connection.commit()
	cursorObj.close()

def db_select(database, query, silent = False):
	global silent_prints
	if not silent:
		print(re.sub('\s+', ' ', query))
	else:
		silent_prints += 1
		if silent_prints % 50 == 0:
			print('.', end = ('' if silent_prints % 500 != 0 else '\n'))
	connection = sqlite3.connect(database)
	cursorObj = connection.cursor()

	rows = cursorObj.execute(query)
	results = []
	for row in rows:
		results.append(row)
	connection.commit()
	cursorObj.close()
	return results