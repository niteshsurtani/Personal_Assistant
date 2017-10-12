from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

def checkRangeIdentifier(word):
	try:
		db_config = read_db_config()
		# db_config['database'] = "travel"
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		command = "SELECT * FROM argument_filler_identifiers WHERE identifier = '" + word + "'"
		cursor.execute(command)

		rows = cursor.fetchall()
		if rows:
			return True
		return False
		
	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()

def checkUnitIdentifier(word):
	try:
		db_config = read_db_config()
		# db_config['database'] = "travel"
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		command = "SELECT * FROM argument_filler_units WHERE units = '" + word + "'"
		cursor.execute(command)
		
		rows = cursor.fetchall()
		if rows:
			return True
		return False
		
	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
