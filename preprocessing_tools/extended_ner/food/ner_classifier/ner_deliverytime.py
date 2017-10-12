from FILE_CONSTANTS import *
import logging
deliverytimeMarker = "DELIVERY TIME"
# check for words whose ner == DURATION
# returns 1 if present, 0 otherwise
def existsDuration(extendedNERAnalyzedParse):
	
	identifierMatch = 0
	fl = 0
	for key in extendedNERAnalyzedParse.keys():
	    	if extendedNERAnalyzedParse[key]["NER"] == 'DURATION':	
				identifierMatch = 1
				fl = 1
				break
	if(fl == 1): 
		return 1			
# return list of terms whose NER == DURATION
def getDuration(extendedNERAnalyzedParse):
	duration_terms = []
	tokenDur=[]
	try:
		for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
			if extendedNERAnalyzedParse[key]["NER"] == 'DURATION':
				if extendedNERAnalyzedParse[key]["NormalizedNER"] not in duration_terms:
					extendedNERAnalyzedParse[key]["NER"] = deliverytimeMarker
					duration_terms.append(extendedNERAnalyzedParse[key]["NormalizedNER"])
					tokenDur.append((key,key+1,extendedNERAnalyzedParse[key]["NormalizedNER"]))
	except:
		logging.exception("error in getDuration")
		duration_terms=[]
		tokenDur=[]
		return tokenDur
	return tokenDur

