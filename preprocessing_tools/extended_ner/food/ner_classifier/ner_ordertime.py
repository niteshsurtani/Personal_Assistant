from FILE_CONSTANTS import *
import logging
ordertimeMarker = "ORDER TIME"

# check for words whose ner == TIME
# returns 1 if present, 0 otherwise
def existsTime(extendedNERAnalyzedParse):
	
	identifierMatch = 0
	fl = 0
	for key in extendedNERAnalyzedParse.keys():
	    	if extendedNERAnalyzedParse[key]["NER"] == 'TIME':	
				identifierMatch = 1
				fl = 1
				break
		if(fl == 1): 
			return 1			
# returns list of terms whose NER == TIME
def getTime(extendedNERAnalyzedParse):
	
	time_terms = []
	tokenTime=[]
	try:
		for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
			if extendedNERAnalyzedParse[key]["NER"] == 'TIME':
				extendedNERAnalyzedParse[key]['NER'] = ordertimeMarker
				time_terms.append(extendedNERAnalyzedParse[key]["NormalizedNER"])
				tokenTime.append((key,key+1,extendedNERAnalyzedParse[key]["NormalizedNER"]))
	except:
		logging.exception("error in getTime")
		time_terms=[]
		tokenTime=[]
		return time_terms,tokenTime
	return time_terms,tokenTime

