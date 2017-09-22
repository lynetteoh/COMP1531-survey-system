import sqlite3

def db_execute(database, expression):
	print(' '.join([x.strip() for x in expression.split(' ')]))
	connection = sqlite3.connect(database)
	cursorObj = connection.cursor()

	cursorObj.execute(expression)
	connection.commit()
	cursorObj.close()

def db_select(database, query):
	print(' '.join([x.strip() for x in query.split(' ')]))
	connection = sqlite3.connect(database)
	cursorObj = connection.cursor()

	rows = cursorObj.execute(query)
	results = []
	for row in rows:
		results.append(row)
	connection.commit()
	cursorObj.close()
	return results