import re
from preprocessing_tools.corenlp.number import *
from preprocessing_tools.extended_ner.travel.api.argument_filler import *

import logging
import nlp_logging
from nlp_logging import logger

from utilities.check_type import isNumber

def isRangeIdentifier(word):
	'''
	(String) -> Boolean

	Takes a word and returns whether it is a range identifier or not.

	INPUT: -,to,and,no
	OUTPUT: True,True,True,False

	'''
	
	try:
		word = word.lower()
		if checkRangeIdentifier(word):
			logger.debug("'%s' is a Range Identifier term", word)
			return True
		return False
	except:
		return False
		
def isUnit(word):
	'''
	(String) -> Boolean

	Takes a word and returns whether it is a unit term or not.

	INPUT: Kilograms,October,no
	OUTPUT: True,True,False

	'''

	word = word.lower()
	if checkUnitIdentifier(word):
		logger.debug("'%s' is a Unit Identifier term", word)
		return True
	return False

def getNumberTokens(tokens):
	count = 0
	numberedTokens = []
	for token in tokens:
		if isNumber(token):
			numberedTokens.append(count)
		count += 1
	return numberedTokens

def fillArguments(query):
	'''
	(String) -> String

	Takes a query with range items missing units, and returns
	the gaps filled with units.

	INPUT: I will be travelling between 25rd and 25th October.
	OUTPUT: I will be travelling between 25rd October and 25th October.

	Cases to handle:
	10 - 15 Kilograms	-> 10 Kilograms - 15 Kilograms
	10 to 15 Kilograms	-> 10 Kilograms to 15 Kilograms
	10 and 15 Kilograms	-> 10 Kilograms and 15 Kilograms
	rupees 10 - 15	-> rupees 10 - rupees 15
	rupees 10 to 15	-> rupees 10 to rupees 15
	rupees 10 and 15	-> rupees 10 and rupees 15
	
	'''

	logger.info("ENTERING GAP FILLER MODULE")
	logger.debug("Query = " + query)

	gap_filled_query = ""

	tokens = query.split()

	numberedTokens = getNumberTokens(tokens)

	to_insert = {}

	for index in range(1,len(numberedTokens)):
		if numberedTokens[index] - numberedTokens[index-1] == 2:
			if isRangeIdentifier(tokens[numberedTokens[index] - 1]):

				boundary = range(0,len(tokens))
				if (numberedTokens[index-1] - 1) in boundary:
					prev_word = tokens[numberedTokens[index-1] - 1]
					if isUnit(prev_word):
						# Copy unit to query
						to_insert[numberedTokens[index]] = prev_word

				if (numberedTokens[index] + 1) in boundary:
					next_word = tokens[numberedTokens[index] + 1]
					if isUnit(next_word):
						# Copy unit to query
						to_insert[numberedTokens[index -1] + 1] = next_word


	gap_filled_tokens = []
	insert_keys = to_insert.keys()
	insert_length = len(insert_keys)
	count = 0

	for index in range(0,len(tokens)):
		if count < insert_length and index == insert_keys[count]:
			gap_filled_tokens.append(to_insert[index])
			logger.debug("Inserted '%s' at index = %d", to_insert[index], index)
			count += 1
		gap_filled_tokens.append(tokens[index])

	gap_filled_query = ' '.join(gap_filled_tokens)
	
	logger.info("GAP FILLING DONE\n")
	return gap_filled_query
