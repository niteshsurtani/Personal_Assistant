from mysql.connector import MySQLConnection, Error
from foodpanda_dbconfig import read_db_config

def insertOneLocality(locality_id, name, city_id, data_resource):
	query = "INSERT INTO locality(locality_id, name, city_id, data_resource) " \
			"VALUES(%s, %s, %s, %s)"

	args = (locality_id, name, city_id, data_resource)

	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		cursor.execute(query, args)

		conn.commit()

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
		print "LOCALITY DATA INSERTED!!!"

def insertManyLocalities(locality_info):
	query = "INSERT INTO locality(locality_id, name, city_id, data_resource) " \
			"VALUES(%s, %s, %s, %s)"

	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		cursor.executemany(query, locality_info)

		conn.commit()

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
		print "LOCALITY DATA INSERTED!!!"

def findLocalityById(id):
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		cursor.execute("SELECT * FROM locality where locality_id = " + id)

		row = cursor.fetchone()
		print row

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()

def findLocalitiesByCityId(id):
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		cursor.execute("SELECT * FROM locality where city_id = " + id)

		rows = cursor.fetchall()
		for row in rows:
			print row
		
	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()

def findLocalityByName(city_id, query):
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		if query: 
			query = query + "%"
			city_id  = str(city_id)
			command = "SELECT * FROM locality WHERE city_id = '" + city_id + "' AND name LIKE '" + query +"'"
			
			cursor.execute(command)

		rows = cursor.fetchall()
		#for row in rows:
		#	print row

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
	return rows
