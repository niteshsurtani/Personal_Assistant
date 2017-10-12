from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

def getTimePeriod(word):
	try:
		db_config = read_db_config()
		# db_config['database'] = "travel"
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		command = "SELECT time_start, time_end FROM time_preference WHERE time_name = '" + word + "'"
		cursor.execute(command)
		
		rows = cursor.fetchall()
		if rows:
			row = rows[0]
			return row
		return ()
		
	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()

def isTimeModifier(word):
	try:
		db_config = read_db_config()
		# db_config['database'] = "travel"
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		command = "SELECT start_percent, end_percent FROM time_preference_modifiers WHERE word = '" + word + "'"
		cursor.execute(command)
		
		rows = cursor.fetchall()
		if rows:
			row = rows[0]
			return row
		return ()
		
	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
