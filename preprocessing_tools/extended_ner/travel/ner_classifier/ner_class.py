import os
import nltk
import re

from PATH_CONSTANTS import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *

# Returns whether the query has CLASS information or not. If NO information of class, then the class
# identification module is not processed further.
def existClass(query):
	tokens = nltk.word_tokenize(query.lower())
	
	identifiers = []
	with open(NO_CLASS_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	
	identifierMatch = 0
	slashFlag = 0
	fl = 0
	for word in identifiers:
		if(word[0] == '-'): 
			slashFlag = 1
		for token in tokens:
			if(slashFlag == 0):
				if(token == word): 
					identifierMatch = 1
					fl = 1
					break
			else:
				if(token[-len(word):] == word):   # Matches last len(word) characters to token
					identifierMatch = 1
					fl = 1
					break
		if(fl == 1): 
			return 1			

# This function reads the RULES file in ner_rules and Returns the seed list of each category.
def loadClassSeedlist(transport):
	content = {}
	with open(TRANSPORT_LIST_FILE) as f:
		for line in f:
			key = line.rstrip()
			content[key] = []
	
	directory = CLASS_SEEDLIST

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

def loadClassTypePatterns(transport,classType):
	classList = []
	
	directory = CLASS_RULES + transport + "/"

	classTypeTokens = classType.split(' ')
	filename = "_".join(classTypeTokens)
	fname = directory+filename+CSV_FILE_EXTENSION

	patterns = []	
	with open(fname) as f:
		line = f.readline().strip()
		patterns = line.split(",")
	return patterns

def matchedClass(query,classValue,classTypePatterns,extendedNERAnalyzedParse):
	lowercaseQuery = query.lower()

	for classType in classTypePatterns:
		searchObj = re.search(classType, lowercaseQuery, re.M|re.I)
		if searchObj:
			identifierWords = classType.split()
			identifierListLength = len(identifierWords)
			tokenId = 0
			tokenId = substrList(identifierWords,identifierListLength,extendedNERAnalyzedParse)
			if tokenId==-1:
				continue
			
			# Change NER for list length
			#print "length ", len(extendedNERAnalyzedParse),identifierWords, tokenId, identifierListLength, extendedNERAnalyzedParse
			for offset in range(0,identifierListLength):
				extendedNERAnalyzedParse[tokenId + offset]["NER"] = classMarker 
				extendedNERAnalyzedParse[tokenId + offset]["NormalizedNER"] = classValue 

			return 1
	return 0

def substrList(identifierList,identifierListLength,extendedNERAnalyzedParse):
	
	startToken = 1
	matchCount = 0
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		if(tokenInfoDict["word"].lower() == identifierList[matchCount]):
			
			if(matchCount == 1):
				#print "-"*50,tokenInfoDict["word"].lower()
				startToken = key
			matchCount = matchCount + 1
			if(matchCount == identifierListLength):
				return startToken

		else:
			matchCount = 0
		startToken += 1
	return -1
	
