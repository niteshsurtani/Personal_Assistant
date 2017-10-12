import re
import sys

import logging
import nlp_logging
from nlp_logging import logger

from utilities.check_type import isNumber

date_extensions = ['st','nd','rd','th']

def split_dot(word):
	try:

		# going.I 	-> going . I
		p1 = re.compile("([A-Za-z]+)(\.)([A-Za-z]+)")

		# 50Kg.	->	50 Kg
		# 4:00am. -> 4 am
		p2 = re.compile("([0-9\:]+)([A-Za-z]+)(\.)")

		# Rs.50	->	Rs 50
		p3 = re.compile("([A-Za-z]+)(\.)([0-9]+)")

		# Rs50	->	Rs 50
		p4 = re.compile("([A-Za-z]+)([0-9]+)")

		# 50Kg	->	50 Kg
		# 4:00am -> 4 am
		p5 = re.compile("([0-9\:]+)([A-Za-z]+)")

		# END.	->	END .
		p6 = re.compile("([A-Za-z]+)(\.)")

		if p1.match(word):
			# print "Match 1"
			return re.sub(p1,r"\1 \2 \3",word)

		elif p2.match(word):
			# print "Match 2"
			return re.sub(p2,r"\1 \2",word)

		elif p3.match(word):
			# print "Match 3"
			return re.sub(p3,r"\1 \3",word)

		elif p4.match(word):
			# print "Match 4"
			return re.sub(p4,r"\1 \2",word)

		elif p5.match(word):
			# print "Match 5"
			new_word = re.sub(p5,r"\1 \2",word)
			tokens = new_word.split(" ")
			if tokens[1] in date_extensions:
				return tokens[0]+tokens[1]
			return new_word

		elif p6.match(word):
			# print "Match 6"
			return re.sub(p6,r"\1 \2",word)

		return word
	
	except:
		logger.error(sys.exc_info()[1])
		return word

def split_hypen(word):
	try:
		words = word.split('-')

		# Check if word is not '-' 
		if len(words) == 2 and words[0] and words[1]:
			# If hypen between two numbers, keep it
			w11 = words[0][len(words[0])-1]
			w12 = words[0][0] 
			w2 = words[1][0]
			firstTen = range(0,10)
			
			if (isNumber(w11) or isNumber(w12)) and isNumber(w2):
				new_words = [words[0],"-",words[1]]
				return new_words
			
			return words
		return [word]
	except:
		logger.error(sys.exc_info()[1])
		return word

def split_word(word):
	try:
		new_word = ""
		splitted_hypen_terms = split_hypen(word)
		# print "Hypen = ",
		# print splitted_hypen_terms
		for term in splitted_hypen_terms:
			splitted_dot_terms = split_dot(term)
			new_word += splitted_dot_terms + " "

		new_word = new_word.strip()
		if new_word != word:
			logger.debug("%s --> %s", word, new_word)
		return new_word

	except:
		logger.error(sys.exc_info()[1])
		return word

def splitNumberString(query):
	'''
	(String) -> String

	Takes a query where multiple word are clubbed together in single token
	and separates such tokens to multiple words.

	INPUT: My budget is Rs.50 and extra luggage 10-15kgs.
	OUTPUT: My budget is Rs 50 and extra luggage 10 - 15 kgs.

	Cases to handle:
	Rs.50	->	Rs 50
	Rs50	->	Rs 50
	10-15kgs	-> 10 - 15 Kgs
	10Kgs-15kgs	-> 10 Kgs - 15 Kgs
	10Kg. 	-> 10 Kg
	10.1	-> 10.1
	10-12-2015	-> 10-12-2015
	10.12.2015	-> 10.12.2015
	END.	-> END .
	one-way -> one way
	1-tier	-> 1 tier
	4:00am	-> 4:00 am
	going.I 	-> going . I
	// Handle ticket/pnr no. and don't split them

	Rules (in order):
	1. Split '-' ---> 10-15 -> 10 - 15, if tier, way -> remove '-', handle date case
	2. Case '.', (i) two numbers: do nothing, (ii) two words: split, (iii) one word-one num: split and remove '.'
	3. Split NUM and String. If last char == '.', if word in dict -> remove '.', else full stop. If split == 'nd' (for date), delete token
	'''

	splitted_query = ""
	logger.info("ENTERING SPLITTER MODULE")
	
	try:
		logger.debug("Query = " + query)

		tokens = query.split()
		for token in tokens:
			splitted_word = split_word(token)
			splitted_query += splitted_word + " "
		
		splitted_query = splitted_query.strip()
		
		logger.info("SPLITTING DONE\n")
		return splitted_query
		
	except:
		logger.error(sys.exc_info()[1])
		logger.info("SPLITTING DONE\n")
		return query
