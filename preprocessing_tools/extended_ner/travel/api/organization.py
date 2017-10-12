from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

def findAllOrganizations():
    	rows = []
	try:

		db_config = read_db_config()
		db_config['database'] = "travel"
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		cursor.execute("SELECT name FROM organization")

		rows = cursor.fetchall()
		return rows

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()

def findOrganizationByName(query):
	rows = []
	try:
		db_config = read_db_config()
		db_config['database'] = "travel"
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		if query: 
			query = query + "%"
			command = "SELECT * FROM organization WHERE name LIKE '" + query +"'"
			#print command
			cursor.execute(command)
		
		rows = cursor.fetchall()
		return rows

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
