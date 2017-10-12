from FILE_CONSTANTS import *
import logging

VOLUME_EXIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/units/volume"
volumeMarker = "VOLUME"
VOL_STANDARD_UNIT = "litre"

# looks for valid volume prefixes
# return 1 if present, 0 otherwise
def existVolume(extendedNERAnalyzedParse):
	
	identifiers = []
	with open(VOLUME_EXIST_FILE) as f:
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

# return numberterm found before the volume prefix, and changes the NormalizedNER of the number term accordingly
# all units are converted to standard unit(litres)
def getVolume(extendedNERAnalyzedParse):
	identifiers = {}
	with open(VOLUME_EXIST_FILE) as f:
		for line in f:
		    	token = line[:-1].split(',')
			identifiers[token[0]] = {'multiplier' : token[1],'keywords': []}
			filename = EXTENDER_NER_DIRECTORY + "food/ner_rules/units/" + token[0]
			with open(filename) as f2:
				for line2 in f2:
				    	identifiers[token[0]]['keywords'].append(line2.rstrip())
	
	units_terms = []
	matched_tokens=[]
	try:
		for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
			word = tokenInfoDict["word"].lower()
			for vol_units in identifiers.keys():
				if word in identifiers[vol_units]['keywords']:
					tokenId = key
					extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"] = str(float(extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"])/float(identifiers[vol_units]['multiplier']))
					units_term_string = extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"]
					extendedNERAnalyzedParse[tokenId-1]["NER"] = volumeMarker
					extendedNERAnalyzedParse[tokenId-1]["NormalizedNER"] = units_term_string
					matched_tokens.append((tokenId-1,tokenId,units_term_string))
					units_terms.append(units_term_string)
	except:
		logging.exception("error in getVolume!")
		units_terms=[]
		matched_tokens=[]
		return units_terms,matched_tokens

	return units_terms,matched_tokens


