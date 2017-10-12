from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

def findPreferences(word):
	try:
		db_config = read_db_config()
		# db_config['database'] = "travel"
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		if word: 
			word = word + "%"
			command = "SELECT word,mapping FROM other_preference WHERE word LIKE '%" + word +"'"
			cursor.execute(command)
		
		rows = cursor.fetchall()
		return rows
		
	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
