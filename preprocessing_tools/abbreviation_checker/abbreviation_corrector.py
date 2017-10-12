import sys
import os
from preprocessing_tools.extended_ner.travel.api.abbreviation_corrector import *

import logging
import nlp_logging
from nlp_logging import logger

def expandWord(word):
	'''
	(String) -> String

	Takes a abbreviated word as input and returns the expanded word.

	INPUT: hyd, kg, rs
	OUTPUT: hyderabad, kilogram, rupees

	'''

	try:
		expanded_word = findWordByAbbreviation(word)
		if expanded_word != '':
			logger.debug("'%s' --> '%s' ", word, expanded_word)
			return expanded_word
		return word
	except:
		logger.error(sys.exc_info()[1])
		return word

def correctAbbreviation(query):
	'''
	(String) -> String

	Takes a query with abbreviations and resolves them into their counterpart.

	INPUT: I want to travel from hyd to blr on 2 oct.
	OUTPUT: I want to travel from Hyderabad to Bangalore on 2 October.

	'''

	abbreviated_query = ""
	logger.info("ENTERING ABBREVIATION CORRECTION MODULE")
	
	try:
		logger.debug("Query = " + query)

		tokens = query.split()
		for token in tokens:
			expanded_word = expandWord(token)
			abbreviated_query += expanded_word + " "
		
		abbreviated_query = abbreviated_query.strip()
		
		logger.info("ABBREVIATION CORRECTION DONE\n")
		return abbreviated_query
	
	except:
		logger.error(sys.exc_info()[1])
		logger.info("ABBREVIATION CORRECTION DONE\n")
		return query
