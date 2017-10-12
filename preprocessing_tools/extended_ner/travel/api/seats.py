from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

def isSeatIdentifier(word):
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		command = "SELECT word FROM seat_identifier WHERE word = '" + word + "'"
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

def getSeatClass(word):
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		command = "SELECT class FROM seat_class WHERE word = '" + word + "'"
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
