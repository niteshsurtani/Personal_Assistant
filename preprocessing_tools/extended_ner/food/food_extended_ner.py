from ner_classifier.classifier import *
import logging


#query = "I want 1 large Dominos pizza, 1 coke and garlic bread."
#category = "food"
from FILE_CONSTANTS import *

CATEGORIES = ['RESTAURANT','FOOD','budget','delivery fee','minimum order','CITY','LOCALITY','ORDER TIME','DELIVERY TIME','CUISINE','PREFERENCE','MEAL','PAYMENT MODE']

def identifyExtendedNER(query,extendedNERAnalyzedParse,chunkedParse):
	entitiesList={}
	entitiesList["CUISINE"]=extractCuisine(extendedNERAnalyzedParse)
	logging.info("cuisine info done")
	entitiesList["VOLUME"],entitiesList["weight"],entitiesList["size"]=extractUnits(extendedNERAnalyzedParse)
	disambiguateAmount(extendedNERAnalyzedParse, chunkedParse)
	logging.info("amount info done.")
	entitiesList["ORDER TIME"]=extractOrderTime(extendedNERAnalyzedParse)
	entitiesList["DELIVERY TIME"]=extractDeliveryTime(extendedNERAnalyzedParse)
	entitiesList["FOOD"]=extractFoodItems(query,extendedNERAnalyzedParse,chunkedParse)
	entitiesList["PREFERENCE"]=extractPreference(extendedNERAnalyzedParse)
	entitiesList["MEAL"]=extractMeal(extendedNERAnalyzedParse)
	entitiesList["PAYMENT MODE"]=extractPaymentMode(extendedNERAnalyzedParse)
	#print extendedNERAnalyzedParse
	entitiesList["CITY"],entitiesList["LOCALITY"]=extractLocation(extendedNERAnalyzedParse)
	#print extendedNERAnalyzedParse
	entitiesList["RESTAURANT"]=extractRestaurant(extendedNERAnalyzedParse)
	logging.info("NER extraction done.")
	print
	print "========================== LIST OF ANALYZED ENTITIES ===================================="
	print entitiesList
	print
	return entitiesList
	# print extendedNERAnalyzedParse

#case of amounts is not handled
def disambiguateTokens(extendedNERAnalyzedParse,entitiesList):
	for token in range(1,len(extendedNERAnalyzedParse)+1):
		#print token, extendedNERAnalyzedParse
		length=0
		for entity in entitiesList:
			for span in entitiesList[entity]:
				if token in range(span[0],span[1]) and span[1]-span[0]>=length:
					length=span[1]-span[0]
					extendedNERAnalyzedParse[token]["NER"]=entity
					extendedNERAnalyzedParse[token]["NormalizedNER"]=span[2]
		#print length, token
		#print extendedNERAnalyzedParse[token]
		#print extendedNERAnalyzedParse[token]["NER"]
		if length==0 and extendedNERAnalyzedParse[token]["NER"]=='0':
			extendedNERAnalyzedParse[token]["NER"]='0'
			extendedNERAnalyzedParse[token]["NormalizedNER"]='0'
	return printextendedNERAnalyzedParse(extendedNERAnalyzedParse)

def printextendedNERAnalyzedParse(extendedNERAnalyzedParse):
	# print " ===================== TEST ==============================="
	# print extendedNERAnalyzedParse
	nerDF = {}
	for index in CATEGORIES:
		nerDF[index] = []
	for key in extendedNERAnalyzedParse.keys():
		if extendedNERAnalyzedParse[key]["NER"] != 'O' and extendedNERAnalyzedParse[key]["NER"]  in CATEGORIES:
			# nerDF[extendedNERAnalyzedParse[key]["NER"]].append(extendedNERAnalyzedParse[key]["NormalizedNER"])
			if key < len(extendedNERAnalyzedParse) and extendedNERAnalyzedParse[key+1]["NER"] != extendedNERAnalyzedParse[key]["NER"]:
				nerDF[extendedNERAnalyzedParse[key]["NER"]].append(extendedNERAnalyzedParse[key]["NormalizedNER"])
			elif key == len(extendedNERAnalyzedParse):
				nerDF[extendedNERAnalyzedParse[key]["NER"]].append(extendedNERAnalyzedParse[key]["NormalizedNER"])
	# print " ===================================== NER ==================="
	# print nerDF	
	# print "==========================================================="
	return nerDF
