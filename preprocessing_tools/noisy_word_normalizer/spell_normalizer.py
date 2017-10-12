import sys
import os
from preprocessing_tools.extended_ner.travel.api.spell_normalizer import *

import logging
import nlp_logging
from nlp_logging import logger

def normalize(word):

	'''
	(String) -> String

	Takes a noisy word as input and returns normalized word.

	INPUT: nah, yeah
	OUTPUT: no, yes

	'''

	logger.info("ENTERING SPELL NOISY NORMALIZER MODULE")

	try:
		normalized_word = findWordByAbbreviation(word)
		return_word = ""
		if normalized_word != '':
			logger.debug("'%s' --> '%s' ", word, normalized_word)
			return_word = normalized_word

		logger.info("SPELL NORMALIZATION DONE\n")
		return return_word
	
	except:
		logger.error(sys.exc_info()[1])
		logger.info("SPELL NORMALIZATION DONE\n")
		return word
