from FILE_CONSTANTS import *
from preprocessing_tools.extended_ner.travel.api.city import *
from utilities.match_longest_string import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *

import logging
import nlp_logging
from nlp_logging import logger

def findCity(extendedNERAnalyzedParse):
	'''
	(Object) -> Object

	Takes the NER Parse as input and annotates the city code corresponding to the city at each city token.
	The city list is loaded from the database matching the first token of city name.

	INPUT: new delhi, new francisco, mumbai
	OUTPUT: DEL, no, BOM

	'''

	logger.info("ENTERING CITY IDENTIFICATION MODULE")

	ner_city = []

	for key in extendedNERAnalyzedParse.keys():   
		if extendedNERAnalyzedParse[key]["NER"] == "0" and extendedNERAnalyzedParse[key]["POS"] in ["NN","NNP","JJ"]:
			token = extendedNERAnalyzedParse[key]["word"]
			matched_cities = findCityByName(token)
			for city_tuple in matched_cities:
				city_code = city_tuple[0]
				city = city_tuple[1]
				if matchLongestString(extendedNERAnalyzedParse,key,city):
					annotateParse(extendedNERAnalyzedParse,key,city,city_code,cityMarker)
					ner_city.append(city_code)
					logger.debug("City Identified = '%s' with code = '%s'", city, city_code)

	logger.info("CITY IDENTIFICATION DONE")
	return ner_city
