from mysql.connector import MySQLConnection, Error
from foodpanda_dbconfig import read_db_config

# def insertOneCity(city_id, name, data_resource):
# 	query = "INSERT INTO city(city_id, name, data_resource) " \
# 			"VALUES(%s, %s, %s)"

# 	args = (city_id, name, data_resource)

# 	try:
# 		db_config = read_db_config()
# 		conn = MySQLConnection(**db_config)

# 		cursor = conn.cursor()
# 		cursor.execute(query, args)

# 		conn.commit()

# 	except Error as error:
# 		print error

# 	finally:
# 		cursor.close()
# 		conn.close()
# 		print "CITY DATA INSERTED!!!"

# def insertManyCities(city_info):
# 	query = "INSERT INTO city(city_id, name, data_resource) " \
# 			"VALUES(%s, %s, %s)"

# 	try:
# 		db_config = read_db_config()
# 		conn = MySQLConnection(**db_config)

# 		cursor = conn.cursor()
# 		cursor.executemany(query, city_info)

# 		conn.commit()

# 	except Error as error:
# 		print error

# 	finally:
# 		cursor.close()
# 		conn.close()
# 		print "CITY DATA INSERTED!!!"

# def findCityById(id):
# 	try:
# 		db_config = read_db_config()
# 		conn = MySQLConnection(**db_config)

# 		cursor = conn.cursor()
# 		cursor.execute("SELECT * FROM city WHERE city_id = " + id)

# 		row = cursor.fetchone()
# 		print row

# 	except Error as error:
# 		print error

# 	finally:
# 		cursor.close()
# 		conn.close()

def findAllCities():
    	rows = []
	try:

		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		cursor.execute("SELECT name FROM city")

		rows = cursor.fetchall()
		# for row in rows:
		# 	print row

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
	return rows

def findCityByName(query):
	rows = []
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		if query: 
			query = query + "%"
			command = "SELECT * FROM city WHERE name LIKE '%" + query +"'"
			#print command
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
