from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

def findWordByAbbreviation(word):
	try:
		db_config = read_db_config()
		# db_config['database'] = "travel"
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		command = "SELECT normalized_word FROM spell_normalizer WHERE noisy_word = '" + word + "'"
		cursor.execute(command)
		
		rows = cursor.fetchall()
		if rows:
			row = rows[0]
			return row[0]
		return ''
		
	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
