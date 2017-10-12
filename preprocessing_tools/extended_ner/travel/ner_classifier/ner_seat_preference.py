import os
import nltk
import re

from PATH_CONSTANTS import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *

def existsSeatPreference(query):
	tokens = nltk.word_tokenize(query)
	
	identifiers = []
	with open(NO_SEAT_PREFERENCE_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	
	identifierMatch = 0
	fl = 0
	for word in identifiers:
		for token in tokens:
			token = token.lower()
			if(token == word): 
				identifierMatch = 1
				fl = 1
				break
		if(fl == 1): 
			return 1			


# This function reads the RULES file in ner_rules and Returns the seed list of each category.
def loadSeatSeedlist(transport):
	content = {"bus": [], "train": [], "flight": []}
		
	directory = SEAT_PREFERENCE_SEEDLIST

	if(transport != "all"):
		filename = transport
		fname = directory+filename
		seed = []
		with open(fname) as f:
			for line in f:
				seed.append(line.rstrip())
			content[transport]=seed
		return content
	
	else:
		for key in content:
			filename = key
			fname = directory+filename
			seed = []
			with open(fname) as f:
				for line in f:
					seed.append(line.rstrip())
				content[key]=seed
		return content

def loadSeatTypePatterns(transport,seatType):
	seatList = []
	
	directory = SEAT_PREFERENCE_RULES + transport + "/"

	seatTypeTokens = seatType.split(' ')
	filename = "_".join(seatTypeTokens)
	fname = directory+filename+CSV_FILE_EXTENSION

	patterns = []	
	with open(fname) as f:
		line = f.readline().strip()
		patterns = line.split(",")
	return patterns

def matchedSeat(query,seatValue,seatTypePatterns,extendedNERAnalyzedParse):
	lowercaseQuery = query.lower()

	for seatType in seatTypePatterns:
		searchObj = re.search(seatType, lowercaseQuery, re.M|re.I)
		if searchObj:
			identifierWords = seatType.split()
			identifierListLength = len(identifierWords)
			tokenId = 0
			tokenId = substrList(identifierWords,identifierListLength,extendedNERAnalyzedParse)
			if tokenId==-1:
				continue
			
			# Change NER for list length
			for offset in range(0,identifierListLength):
				extendedNERAnalyzedParse[tokenId + offset]["NER"] = seatMarker 
				extendedNERAnalyzedParse[tokenId + offset]["NormalizedNER"] = seatValue 

			return 1
	return 0

def substrList(identifierList,identifierListLength,extendedNERAnalyzedParse):
	
	startToken = 1
	matchCount = 0
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		if(tokenInfoDict["word"].lower() == identifierList[matchCount]):
			
			if(matchCount == 1):
				startToken = key
			matchCount = matchCount + 1
			if(matchCount == identifierListLength):
				return startToken

		else:
			matchCount = 0
		startToken += 1
	return -1
	