import os
import nltk
import re

from xml.dom import minidom

from PATH_CONSTANTS import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *
# Returns whether the query has CLASS information or not. If NO information of class, then the class
# identification module is not processed further.

def tatkalbooking(query,extendedNERAnalyzedParse):
	identifiers = []
	with open(TRAIN_QUOTA_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	
	identifierMatch = 0
	fl = 0
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		word = tokenInfoDict["word"].lower()
		if word in identifiers:
			tokenId = key
			extendedNERAnalyzedParse[tokenId]["NER"] = trainQuotaMarker 
					
			identifierMatch = 1
			fl = 1
			break
		if(fl == 1): 
			return 1			





