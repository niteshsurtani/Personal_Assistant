from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

# def insertOneDish(dish_id, restaurant_id, dish_name, type, cost, data_resource):
# 	query = "INSERT INTO menu(dish_id, restaurant_id, dish_name, cost, type, data_resource) " \
# 			"VALUES(%s, %s, %s, %s, %s, %s)"

# 	args = (dish_id, restaurant_id, dish_name, cost, type, data_resource)

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
# 		print "DISHES DATA INSERTED!!!"

# def insertManyDishes(menu_info):
# 	query = "INSERT INTO menu(dish_id, restaurant_id, dish_name, type, cost, data_resource) " \
# 			"VALUES(%s, %s, %s, %s, %s, %s)"

# 	try:
# 		db_config = read_db_config()
# 		conn = MySQLConnection(**db_config)

# 		cursor = conn.cursor()
# 		cursor.executemany(query, menu_info)

# 		conn.commit()

# 	except Error as error:
# 		print error

# 	finally:
# 		cursor.close()
# 		conn.close()
# 		print "DISHES DATA INSERTED!!!"

# def findDishById(id):
# 	try:
# 		db_config = read_db_config()
# 		conn = MySQLConnection(**db_config)

# 		cursor = conn.cursor()
# 		cursor.execute("SELECT * FROM menu where dish_id = " + id)

# 		row = cursor.fetchone()
# 		print row

# 	except Error as error:
# 		print error

# 	finally:
# 		cursor.close()
# 		conn.close()

# def findDishesByRestaurantId(id):
# 	try:
# 		db_config = read_db_config()
# 		conn = MySQLConnection(**db_config)

# 		cursor = conn.cursor()
# 		cursor.execute("SELECT * FROM menu where restaurant_id = " + id)

# 		rows = cursor.fetchall()
# 		return rows

# 	except Error as error:
# 		print error

# 	finally:
# 		cursor.close()
# 		conn.close()

def findDishByName(query):
	rows = []
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		if query: 
			query = query + "%"
		cursor.execute("SELECT dish_name FROM dish WHERE dish_name LIKE '%s'" % query)

		rows = cursor.fetchall()
	#	for row in rows:
	#		print row

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
	return rows
