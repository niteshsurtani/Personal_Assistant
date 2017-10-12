import os
import sys
from preprocessing_tools.extended_ner.travel.api.normalizer import *

import logging
import nlp_logging
from nlp_logging import logger


def get_normalized_word(word):
	'''
	(String) -> String

	Takes a noisy word as input and returns normalized word.

	INPUT: b4, 2morrow, uttar, going
	OUTPUT: before, tomorrow, uttar, ''

	'''

	try:
		normalized_word = findWordByAbbreviation(word)
		if normalized_word != '':
			logger.debug("'%s' --> '%s' ", word, normalized_word)
			return normalized_word
		return word
	except:
		logger.error(sys.exc_info()[1])
		return word

def normalize(query):

	'''
	(String) -> String

	Takes a noisy query as input and returns normalized query.

	INPUT: I wanna go to hyderabad 2morrow
	OUTPUT: I want to go to hyderabad tomorrow 

	'''
	
	normalized_query = ""
	logger.info("ENTERING NOISY NORMALIZER MODULE")

	try:
		logger.debug("Query = " + query)

		tokens = query.split()
		for token in tokens:
			normalized_word = get_normalized_word(token)
			normalized_query += normalized_word + " "
		
		normalized_query = normalized_query.strip()
	
		logger.info("NORMALIZATION DONE\n")
		return normalized_query
	
	except:
		logger.error(sys.exc_info()[1])
		logger.info("NORMALIZATION DONE\n")
		return query
