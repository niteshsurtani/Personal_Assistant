import os
import nltk
import re

from xml.dom import minidom

from PATH_CONSTANTS import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *
# Returns whether the query has CLASS information or not. If NO information of class, then the class
# identification module is not processed further.

def existWeight(query):
	tokens = nltk.word_tokenize(query)
	
	identifiers = []
	with open(WEIGHT_EXIST_FILE) as f:
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

def getWeights(extendedNERAnalyzedParse):
	identifiers = []
	with open(WEIGHT_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	
	weight_terms = []

	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		word = tokenInfoDict["word"].lower()
		if word in identifiers:
			tokenId = key

			weight_term_string = extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"]
			
			extendedNERAnalyzedParse[tokenId-1]["NER"] = weightMarker			
			extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"] = weight_term_string

			extendedNERAnalyzedParse[tokenId]["NER"] = weightMarker
			extendedNERAnalyzedParse[tokenId]["NormalizedNER"] = weight_term_string

			weight_terms.append(weight_term_string)
	return weight_terms	


