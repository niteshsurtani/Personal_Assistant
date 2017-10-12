import os

from PATH_CONSTANTS import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *
from preprocessing_tools.extended_ner.travel.api.round_trip import *
from utilities.match_longest_string import *
	
import logging
import nlp_logging
from nlp_logging import logger

def TravelType(extendedNERAnalyzedParse, last_requested_DF):
	'''
	(Object) -> Object

	Takes the NER Parse as input and annotates the round_trip code corresponding 
	to the round_trip at each round_trip token.
	The round_trip list is loaded from the database matching the first token of round_trip name.

	INPUT: one way, 2-way, returning
	OUTPUT: 0,1,1
	'''

	logger.info("ENTERING ROUND TRIP IDENTIFICATION MODULE")

	checkFlag = 1

	if last_requested_DF == travelTypeMarker.lower():
		key = 1
		word = extendedNERAnalyzedParse[key]['word'].lower()

		if(word == "yes"):
			annotateParse(extendedNERAnalyzedParse,key,word,"1",travelTypeMarker)
			checkFlag = 0
			logger.debug("Round Trip identifier = '%s' with code = '%s'", word, "1")

		elif(word == "no"):
			annotateParse(extendedNERAnalyzedParse,key,word,"0",travelTypeMarker)
			checkFlag = 0
			logger.debug("Round Trip identifier = '%s' with code = '%s'", word, "0")
	
	if checkFlag:
		for key in extendedNERAnalyzedParse.keys():   
			word = extendedNERAnalyzedParse[key]["word"]
			lemma = extendedNERAnalyzedParse[key]["lemma"]

			matched_round_trip = findRoundTrip(word,lemma)
			for round_trip_tuple in matched_round_trip:
				round_trip_code = round_trip_tuple[0]
				round_trip = round_trip_tuple[1]

				if matchLongestString(extendedNERAnalyzedParse,key,round_trip):
					annotateParse(extendedNERAnalyzedParse,key,round_trip,round_trip_code,travelTypeMarker)
					logger.debug("Round Trip identifier = '%s' with code = '%s'", round_trip, round_trip_code)

	logger.info("ROUND TRIP IDENTIFICATION DONE")