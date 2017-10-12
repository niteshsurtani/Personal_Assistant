from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

def getRangeIdentifier(word):
	rows = []
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		if word: 
			word = word + "%"
			command = "SELECT word, category FROM range_identifiers WHERE word LIKE '%" + word +"'"
			#print command
			cursor.execute(command)
		
		rows = cursor.fetchall()
		return rows

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()

def getNERSemantics(ner):
	try:
		db_config = read_db_config()
		# db_config['database'] = "travel"
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		command = "SELECT minimum, maximum FROM ner_config WHERE category = '" + ner + "'"
		cursor.execute(command)
		
		rows = cursor.fetchall()
		if rows:
			row = rows[0]
			return row
		return ''
		
	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
