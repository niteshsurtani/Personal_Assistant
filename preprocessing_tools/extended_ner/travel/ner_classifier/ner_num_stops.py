from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *
from PATH_CONSTANTS import *

from preprocessing_tools.extended_ner.travel.api.stops import *
from utilities.match_longest_string import *

import logging
import nlp_logging
from nlp_logging import logger

windowSize = 3
stopLimit = 6

def findNumberToken(extendedNERAnalyzedParse):
	stopsList = []
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		if((tokenInfoDict["NER"] == "NUMBER" and float(tokenInfoDict["NormalizedNER"]) < float(stopLimit)) or tokenInfoDict["word"].lower() == "no"):
			stopsList.append(key)
	return stopsList

def compareStopList(index, stopsList):
	minValue = 1000
	minIndex = -1
	for val in stopsList:
		if abs(val - index) < minValue:
			minValue = abs(val - index)
			minIndex = val

	if minValue > windowSize:
		return 0
	return minIndex


def getNumStops(extendedNERAnalyzedParse):
	'''
	(Object) -> Object

	Takes the NER Parse as input and annotates the number of stops.

	INPUT: 2 stops, less than 3 stops
	OUTPUT: 2, {0,2}

	'''

	logger.info("ENTERING NUM STOPS IDENTIFICATION MODULE")

	range_dict = {"exact":"","range":{"min":"","max":""}}

	stopsList = findNumberToken(extendedNERAnalyzedParse)
	
	if(len(stopsList) > 0):
		for key in extendedNERAnalyzedParse.keys():   
			word = extendedNERAnalyzedParse[key]["word"]
			lemma = extendedNERAnalyzedParse[key]["lemma"]
			
			stop_word = isStopItem(lemma)
			if stop_word:
				index = compareStopList(key, stopsList)

				if index:
					indexWord = extendedNERAnalyzedParse[index]["word"]
					indexWordValue = extendedNERAnalyzedParse[index]["NormalizedNER"]
					if indexWord.lower() == "no":
						range_dict["exact"] = "0"
					else:
						range_dict["exact"] = indexWordValue

					annotateParse(extendedNERAnalyzedParse,index,indexWord,range_dict,numStopMarker)
					logger.debug("Num Stops Identified = '%s' from word = '%s'", range_dict["exact"], stop_word)
	

	logger.info("NUM STOPS IDENTIFICATION DONE")
