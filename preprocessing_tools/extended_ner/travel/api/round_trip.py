from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def findRoundTrip(word,lemma):
	round_trip = []
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		if word: 
			word = word + "%"
			command = "SELECT type,word FROM round_trip WHERE word LIKE '%" + word +"'"
			#print command
			cursor.execute(command)
		
		rows1 = cursor.fetchall()

		if lemma: 
			lemma = lemma + "%"
			command = "SELECT type,word FROM round_trip WHERE word LIKE '%" + lemma +"'"
			#print command
			cursor.execute(command)
		
		rows2 = cursor.fetchall()

		return union(rows1,rows2)

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()
