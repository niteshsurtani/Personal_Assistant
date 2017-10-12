from FILE_CONSTANTS import *
import logging

WEIGHT_EXIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/units/weight"
weightMarker = "WEIGHT"
WEIGHT_STANDARD_UNIT = "killo-gram"


# return numberterm found before the weight prefix, and changes the NormalizedNER of the number term accordingly
# all units are converted to standard unit(killo-gram)
def getWeight(extendedNERAnalyzedParse):
	identifiers = {}
	with open(WEIGHT_EXIST_FILE) as f:
		for line in f:
		    	token = line[:-1].split(',')
			identifiers[token[0]] = {'multiplier' : token[1],'keywords': []}
			filename = EXTENDER_NER_DIRECTORY + "food/ner_rules/units/" + token[0]
			with open(filename) as f2:
				for line2 in f2:
				    	identifiers[token[0]]['keywords'].append(line2.rstrip())
	
	units_terms = []
	matchedTokens=[]
	try:
		for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
			word = tokenInfoDict["word"].lower()
			for wt_units in identifiers.keys():
				if word in identifiers[wt_units]['keywords']:
					tokenId = key
					extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"] = str(float(extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"])/float(identifiers[wt_units]['multiplier']))
					units_term_string = extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"]
					extendedNERAnalyzedParse[tokenId-1]["NER"] = weightMarker
					extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"] = units_term_string
					matchedTokens.append((tokenId-1,tokenId,units_term_string))
					units_terms.append(units_term_string)
	except:
		logging.exception("error in getWeight")
		units_terms=[]
		matchedTokens=[]
		return units_terms, matchedTokens
	return units_terms, matchedTokens


