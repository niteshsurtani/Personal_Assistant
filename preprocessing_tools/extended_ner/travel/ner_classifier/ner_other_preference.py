from FILE_CONSTANTS import *
from preprocessing_tools.extended_ner.travel.api.other_preference import *
from utilities.match_longest_string import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *

import logging
import nlp_logging
from nlp_logging import logger

def getOtherPreference(extendedNERAnalyzedParse):
	'''
	(Object) -> Object

	Takes the NER Parse as input and annotates the preferences of user like
	shortest, quickest, cheapest flights etc.

	INPUT: shortest, quickest, cheapest flights
	OUTPUT: fastest, fastest, cheapest

	'''

	logger.info("ENTERING OTHER PREFERENCES IDENTIFICATION MODULE")

	for key in extendedNERAnalyzedParse.keys():   
		token = extendedNERAnalyzedParse[key]["word"]
		matched_preferences = findPreferences(token)
		for preference_tuple in matched_preferences:
			preference_name = preference_tuple[0]
			preference_type = preference_tuple[1]

			if matchLongestString(extendedNERAnalyzedParse,key,preference_name):
				annotateParse(extendedNERAnalyzedParse,key,preference_name,preference_type,otherPreferenceMarker)
				logger.debug("Other preferences Identified = '%s' with type = '%s'", preference_name,preference_type)

	logger.info("OTHER PREFERENCES IDENTIFICATION DONE")
