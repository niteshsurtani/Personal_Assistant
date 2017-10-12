from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *
from PATH_CONSTANTS import *

from preprocessing_tools.extended_ner.travel.api.results import *
from utilities.match_longest_string import *

import logging
import nlp_logging
from nlp_logging import logger

maxResult = 10
windowSize = 3

def findNumberToken(extendedNERAnalyzedParse):
	resultsList = []
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		if((tokenInfoDict["NER"] == "NUMBER" and float(tokenInfoDict["NormalizedNER"]) < float(maxResult))):
			resultsList.append(key)
	return resultsList

def compareResultList(index, resultsList):
	for val in resultsList:
		if index - val < windowSize:
			return val
	return 0


def getNumResults(extendedNERAnalyzedParse):
	'''
	(Object) -> Object

	Takes the NER Parse as input and annotates the number of flight results to display.

	INPUT: 2 flights, 3 cheapest flights
	OUTPUT: 2, 3

	'''

	logger.info("ENTERING NUM RESULTS IDENTIFICATION MODULE")

	resultsList = findNumberToken(extendedNERAnalyzedParse)
	
	if(len(resultsList) > 0):
		for key in extendedNERAnalyzedParse.keys():   
			word = extendedNERAnalyzedParse[key]["word"]
			lemma = extendedNERAnalyzedParse[key]["lemma"]
			
			result_word = isResultItem(lemma)
			if result_word:

				index = compareResultList(key, resultsList)

				if index:
					indexWord = extendedNERAnalyzedParse[index]["word"]
					indexWordValue = extendedNERAnalyzedParse[index]["NormalizedNER"]

					annotateParse(extendedNERAnalyzedParse,index,indexWord,indexWordValue,numResultMarker)
					logger.debug("Num Results Identified = '%s' from word = '%s'", indexWordValue, result_word)
	

	logger.info("NUM RESULTS IDENTIFICATION DONE")
