from FILE_CONSTANTS import *
 

MEAL_EXIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/meal/meal_list"
mealMarker = "MEAL"

def findMeal(extendedNERAnalyzedParse):
	
	identifiers = []
	with open(MEAL_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	for key in extendedNERAnalyzedParse.keys():
		token = extendedNERAnalyzedParse[key]['word'].lower()
		for word in identifiers:
			if(token == word): 
				extendedNERAnalyzedParse[key]["NER"] = mealMarker
				extendedNERAnalyzedParse[key]["NormalizedNER"] = word
				return [(key,key+1,word)]
	return []