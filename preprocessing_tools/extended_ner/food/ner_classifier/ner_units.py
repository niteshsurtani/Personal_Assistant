from FILE_CONSTANTS import *
 

UNITS_EXIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/units/units_list"
unitsMarker = "VOLUME"
VOL_STANDARD_UNIT = "litre"
def existUnits(extendedNERAnalyzedParse):
	
	identifiers = []
	with open(UNITS_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	
	identifierMatch = 0
	fl = 0
	for key in extendedNERAnalyzedParse.keys():
		token = extendedNERAnalyzedParse[key]['word'].lower()
		for word in identifiers:
			if(token == word): 
				identifierMatch = 1
				fl = 1
				break
		if(fl == 1): 
			return 1			

def getUnits(extendedNERAnalyzedParse):
	identifiers = []
	with open(UNITS_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	
	units_terms = []

	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		word = tokenInfoDict["word"].lower()
		if word in identifiers:
			tokenId = key

## write convertor --> standard unit is litres
			if word == 'ml':
			    extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"] = str(float(extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"])/1000)
			units_term_string = extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"]

			extendedNERAnalyzedParse[tokenId-1]["NER"] = unitsMarker
			extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"] = units_term_string

			units_terms.append(units_term_string)
	return units_terms	


