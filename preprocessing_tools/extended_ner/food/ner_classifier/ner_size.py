from FILE_CONSTANTS import *
import logging

SIZE_EXIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/units/size"
sizeMarker = "SIZE"


# return numberterm found before the size prefix, and changes the NormalizedNER of the number term accordingly
# all units are converted to standard unit(killo-gram)
def getSize(extendedNERAnalyzedParse):
	identifiers = {}
	matchedTokens=[]
	with open(SIZE_EXIST_FILE) as f:
		for line in f:
			identifiers = line.split(',')

	units_terms = []
	try:
		for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
			word = tokenInfoDict["word"].lower()

			if word in identifiers:
				extendedNERAnalyzedParse[key]["NER"] = sizeMarker
				extendedNERAnalyzedParse[key]["NormalizedNER"] = word
				units_terms.append(word)
				matchedTokens.append((key,key+1,word))
	except:
		logging.exception("error in getSize")
		units_terms=[]
		matchedTokens=[]
		return units_terms,matchedTokens
	return units_terms,matchedTokens

