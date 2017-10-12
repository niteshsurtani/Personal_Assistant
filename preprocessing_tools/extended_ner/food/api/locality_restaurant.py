from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

def insertOneLocalityRestaurant(locality_id, restaurant_id):
	query = "INSERT INTO locality_restaurant(locality_id, restaurant_id) " \
			"VALUES(%s, %s)"

	args = (locality_id, restaurant_id)

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
		print "LOCALITY_RESTAURANT DATA INSERTED!!!"

def insertManyLocalityRestaurants(locality_restaurant_info):
	query = "INSERT INTO locality_restaurant(locality_id, restaurant_id) " \
			"VALUES(%s, %s)"

	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		cursor.executemany(query, locality_restaurant_info)

		conn.commit()

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
		print "LOCALITY_RESTAURANT DATA INSERTED!!!"

def findRestaurantsByLocalityId(id):
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		cursor.execute("SELECT * FROM locality_restaurant where locality_id = " + id)

		rows = cursor.fetchall()
		for row in rows:
			print row

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()