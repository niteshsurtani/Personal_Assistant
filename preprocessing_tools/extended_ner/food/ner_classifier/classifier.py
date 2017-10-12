from FILE_CONSTANTS import *
from ner_fooditem import *
from ner_amount import *
from ner_volume import *
from ner_weight import *
from ner_size import *
from ner_location import *
from ner_ordertime import *
from ner_deliverytime import *
from ner_cuisine import *
from ner_preference import *
from ner_paymentmode import *
from ner_meal import *
from ner_restaurant import *
from amount_disambiguator import *
from amounts import *
import logging
# from preprocessing_tools.extended_ner.food.api.cuisine_restaurant import *


# looks for city in query, only if city specified looks for locality
# def extractRestaurant(extendedNERAnalyzedParse):
# 	findRestaurant(extendedNERAnalyzedParse)

def extractLocation(extendedNERAnalyzedParse):
	logging.info("Extracting location info.")
	city_id,cityTokens = findCity(extendedNERAnalyzedParse)
	localityTokens=[]
	if len(city_id) >= 0:
		if len(city_id)>0:
			logging.info("Multiple cities found. Searching for locality in all matched cities.")
		for id in city_id:
			locality_index, matched_locality_item_list, matched=findLocality(extendedNERAnalyzedParse,id)
			localityTokens+=locality_index
	return cityTokens,localityTokens
	'''
	if(existsCity(extendedNERAnalyzedParse)):
    		city_list = getCity(extendedNERAnalyzedParse)
#		print "CITY : "
#		print city_list
		locality_list = []
		if (existsLocality(extendedNERAnalyzedParse)):
		    	for city in city_list:
				locality_list.append(getLocality(extendedNERAnalyzedParse,city))
#			print "LOCALITY : "
#			print locality_list
	else:
	    	if(existsLocality(extendedNERAnalyzedParse)):
		    	city_list = loadCityNames()
			locality_list = []
		    	for city in city_list:
				locality_list.append(getLocality(extendedNERAnalyzedParse,city))
			print "LOCALITY : "
			print locality_list
	'''


# Finds and marks amount terms, and disambiguates them into categories - budget, minimum order and delivery fee
def disambiguateAmount(extendedNERAnalyzedParse, chunkedParse):
	logging.info("extracting Amount information")
	numbertokenIdlist = getNumberTokens(extendedNERAnalyzedParse)
#	print "number tokens : "
#	print numbertokenIdlist
	
	amount_terms,tokenAmt = getValueMarkers(extendedNERAnalyzedParse, numbertokenIdlist)
#	print "value terms : "
#	print amount_terms
#	print "currency terms :"
	
	currency_term_list = FindCurrency(extendedNERAnalyzedParse,amount_terms)
#	print currency_term_list

#	print 'Range terms: '
	DetectRange(currency_term_list, extendedNERAnalyzedParse)

	matched_category = GetCategoryKeyWords(extendedNERAnalyzedParse)
#	print "matched_category : "
#	print matched_category
	
#	print "negation : "
	matched_category_values, required_amount_terms_count = FindNegationCategories(matched_category, extendedNERAnalyzedParse, chunkedParse)
#	print matched_category_values
#	print 'amount terms needed: '
#	print required_amount_terms_count
	
	
	amount_tokenId_list,amount_terms_present_count = GetNumberofAmounts(extendedNERAnalyzedParse)
#	print 'amount terms list : '
#	print amount_tokenId_list
#	print 'amount terms found : '
#	print amount_terms_present_count
	if amount_terms_present_count == required_amount_terms_count:
	    	category_amount_values = Merge(matched_category_values,amount_tokenId_list, extendedNERAnalyzedParse)
#		print 'merge  : '
#		print category_amount_values
		return
	elif amount_terms_present_count < required_amount_terms_count:
	    	amount_tokenId_list = UpdateAmountList(extendedNERAnalyzedParse)
#		print 'updated amount terms list : '
#		print amount_tokenId_list
	matched_category_values = MergeNearest(matched_category_values,amount_tokenId_list,extendedNERAnalyzedParse)
#	print 'merge  : '
#	print matched_category_values


# finds and marks volume and weight terms
def extractUnits(extendedNERAnalyzedParse):
	logging.info("Finding volume, weight and size terms")
	vol_terms,matchedVolumeTokens = getVolume(extendedNERAnalyzedParse)

	weight_terms,matchedWeightTokens = getWeight(extendedNERAnalyzedParse)

	size_terms,matchedSizeTokens = getSize(extendedNERAnalyzedParse)
	logging.info("found "+str(len(matchedVolumeTokens))+" volume terms,"+str(len(matchedWeightTokens))+" weight terms,"+str(len(matchedSizeTokens))+" size terms")
	return matchedVolumeTokens, matchedWeightTokens, matchedSizeTokens

# find and marks food items
def extractFoodItems(query,extendedNERAnalyzedParse,chunkedParse):
	logging.info("extracting food items and their attributes")
	matched_token_id_list,matched_food_item_list,flag = FindFoodItems(query,extendedNERAnalyzedParse)
	print matched_token_id_list,matched_food_item_list,flag

	if flag:	

		if not matched_token_id_list:
			logging.info("food items not found!")
		else:
			logging.info("Food items found. Extracting attributes.")
		GetQuantitySize1(extendedNERAnalyzedParse,matched_token_id_list)
		x=0
		for token in extendedNERAnalyzedParse:
			if extendedNERAnalyzedParse[token]["NER"]=="FOOD":
				matched_token_id_list[x][2]=extendedNERAnalyzedParse[token]["NormalizedNER"]
				x+=1
	return matched_token_id_list


def extractRestaurant(extendedNERAnalyzedParse):
	logging.info("Searching for restaurant.")
	restaurant_index, matched_restaurant_item_list, matched = FindRestaurantItems(extendedNERAnalyzedParse)
	return restaurant_index

# find and marks order time using NER == TIME
def extractOrderTime(extendedNERAnalyzedParse):
		logging.info("extracting order time")
		tokenTime=[]
		if(existsTime(extendedNERAnalyzedParse)):
			time_list,tokenTime = getTime(extendedNERAnalyzedParse)
		return tokenTime
#		print "ORDER TIME :"
#		print time_list


# find and marks delivery time using NER == DURATION
def extractDeliveryTime(extendedNERAnalyzedParse):
	logging.info("extracting delivery time")
	if(existsDuration(extendedNERAnalyzedParse)):
		return getDuration(extendedNERAnalyzedParse)
	else:
		return []
#		print "DELIVERY TIME :"
#		print duration_list

# find and marks cuisine terms
def extractCuisine(extendedNERAnalyzedParse):
    #    	findCuisine(extendedNERAnalyzedParse)
	logging.info("extracting cuisine information")
	matched_token_id_list,cuisine_list,flag = findCuisine(extendedNERAnalyzedParse)
	#print matched_token_id_list,cuisine_list
	if not matched_token_id_list:
		logging.info("No cuisine info found!")
	return matched_token_id_list
#	if flag : 
	    #	    print "CUISINE : "
	    #print cuisine_list
#	UpdateCuisineNER(matched_token_id_list,cuisine_list, extendedNERAnalyzedParse)

# finds and marks vegetarian/non-vegetarian preferences
def extractPreference(extendedNERAnalyzedParse):
	logging.info("Finding preferences.")
    	return findPreference(extendedNERAnalyzedParse)
#	if flag:
	    #	print "PREFERENCE  :"
	#    	UpdatePreferenceNER(matched_token_id_list,preference_list, extendedNERAnalyzedParse)

def extractMeal(extendedNERAnalyzedParse):
	logging.info("Identifying meal type.")
    	return findMeal(extendedNERAnalyzedParse)


def extractPaymentMode(extendedNERAnalyzedParse):
	logging.info("Identifying payment mode.")
    	return findPaymentMode(extendedNERAnalyzedParse)
