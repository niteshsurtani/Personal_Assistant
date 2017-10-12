from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *
from PATH_CONSTANTS import *

from preprocessing_tools.extended_ner.travel.api.seats import *
from utilities.match_longest_string import *

import logging
import nlp_logging
from nlp_logging import logger

seatLimit = 6

def findNumberToken(extendedNERAnalyzedParse):
	seatsList = []
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		if(tokenInfoDict["NER"] == "NUMBER" and float(tokenInfoDict["NormalizedNER"]) < float(seatLimit)):
			seatsList.append(key)
	return seatsList

def matchSeatIdentifier(extendedNERAnalyzedParse):
	matchedList = {}
	for key in extendedNERAnalyzedParse.keys():   
		word = extendedNERAnalyzedParse[key]["word"]
		lemma = extendedNERAnalyzedParse[key]["lemma"]
	
		seat_class = getSeatClass(lemma)
		if seat_class:
			matchedList[key] = seat_class

	return matchedList

def mapClassToNumber(extendedNERAnalyzedParse,numList, classDict, template):
	typeList = classDict.keys()

	numLength = len(numList)
	typeLength = len(typeList)

	defaultType = "adults"

	if numLength == typeLength:
		i = 0
		index = numList[i]

		for key, val in classDict.iteritems():
			template[val] = extendedNERAnalyzedParse[index]['NormalizedNER']
			i += 1
		return 1
	
	elif numLength == 1 and typeLength == 0:
		template[defaultType] = numList[0]
		return 1

	return 0


def getNumSeats(extendedNERAnalyzedParse,last_requested_DF):
	'''
	(Object) -> Object

	Takes the NER Parse as input and annotates the number of seats.

	INPUT: 2 tickets; 3 adults, 2 children
	OUTPUT: 2, {3,2}

	'''

	logger.info("ENTERING NUM SEATS IDENTIFICATION MODULE")

	template = {"adults":0,"children":0,"infants":0}

	seatsList = findNumberToken(extendedNERAnalyzedParse)
	
	if(len(seatsList) > 0):
		if len(seatsList) == 1 and last_requested_DF.lower() == numSeatMarker.lower():
			index = seatsList[0]
			indexWord = extendedNERAnalyzedParse[index]["word"]

			template['adults'] = extendedNERAnalyzedParse[index]["NormalizedNER"]
			annotateParse(extendedNERAnalyzedParse,index,indexWord,template,numSeatMarker)
			logger.debug("Num Seats Identified = '%s'", str(template))

		else:
			seat_flag = 0
			for key in extendedNERAnalyzedParse.keys():   
				word = extendedNERAnalyzedParse[key]["word"]
				lemma = extendedNERAnalyzedParse[key]["lemma"]
				
				seat_word = isSeatIdentifier(lemma)
				if seat_word:
					seat_flag = 1
					break
			
			if seat_flag:
				classDict = matchSeatIdentifier(extendedNERAnalyzedParse)

				map_list = mapClassToNumber(extendedNERAnalyzedParse,seatsList, classDict,template)

				if map_list:
					for key in classDict.keys():   
						word = extendedNERAnalyzedParse[key]["word"]
						annotateParse(extendedNERAnalyzedParse,key,word,template,numSeatMarker)
		
				logger.debug("Num Seats Identified = '%s'", str(template))

	logger.info("NUM SEATS IDENTIFICATION DONE")

