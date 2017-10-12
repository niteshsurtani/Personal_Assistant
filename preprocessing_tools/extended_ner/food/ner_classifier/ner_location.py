from FILE_CONSTANTS import *
from preprocessing_tools.extended_ner.food.api.city import *
from preprocessing_tools.extended_ner.food.api.locality import *
import logging
## ASSUMING THAT THE CITY AND LOCALITY NAMES WILL BE CORRECT IN THE extendedNERAnalyzedParse eg: Hyderbad,Gachibowli


# CITY_EXIST_FILE = EXTENDER_NER_DIRECTORY + "locality/database/city_list"
# LOCALITY_EXIST_FILE = EXTENDER_NER_DIRECTORY + "locality/database/locality_list"
localityMarker = 'LOCALITY'
cityMarker = 'CITY'
CITY_FOLDER = EXTENDER_NER_DIRECTORY + "locality/database/city/"

# load city names from database, sets the value of NER and NormalizedNer of the fist word of the city name
# returns city_id of the city detected in query
# def findCity(extendedNERAnalyzedParse):
	
# 	fl = -1
# 	mapped_city=""
# 	for key in extendedNERAnalyzedParse.keys():   
# 		if extendedNERAnalyzedParse[key]["POS"] in ["JJ","NN","NNP","NNS"]:
# 			token = extendedNERAnalyzedParse[key]["word"].lower()
# 			matched_cities = findCityByName(token)
# 			print "-"*100,matched_cities
# 			if matched_cities :
# 				if len(matched_cities) == 1:
# 					matched_city_name = matched_cities[0][1].lower()
# 					matched_city_token = matched_city_name.split()
# 					for w in matched_city_token:
# 						if w == token:
# 							fl = matched_cities[0][0]
# 							mapped_city=matched_cities[0][2]
# 							extendedNERAnalyzedParse[key]['NER'] = cityMarker			
# 							extendedNERAnalyzedParse[key]['NormalizedNER'] = matched_cities[0][2]
# 							print matched_cities[0][2]
# 				else:
# 					for city in matched_cities:
# 						matched_flag = 1
# 						city_name_list = city[1].lower().split()
# 						if len(city_name_list) == 1 and city_name_list[0] == token:
# 							fl = city[0]
# 							mapped_city=city[2]
# 							extendedNERAnalyzedParse[key]['NER'] = cityMarker
# 							extendedNERAnalyzedParse[key]['NormalizedNER'] = city[2]
# 							print city
# 						else:
# 							for i in range(1,len(city_name_list)):
# 								if extendedNERAnalyzedParse[key+i]["word"] != city_name_list[i].lower():
# 									matched_flag = 0
# 							if matched_flag :
# 								fl = city[0]
# 								mapped_city=city[2]
# 								extendedNERAnalyzedParse[key]['NER'] = cityMarker
# 								extendedNERAnalyzedParse[key]['NormalizedNER'] = city[2]
# 								print city
# 	if mapped_city:
# 		fl=findIdByName(mapped_city)[0][0]
# 	#print mapped_city, fl, city
# 	return fl

def findCity(extendedNERAnalyzedParse):
	fl = []
	cityTokens=[]
	try:
		for key in extendedNERAnalyzedParse.keys():
			if extendedNERAnalyzedParse[key]["POS"] in ["JJ","NN","NNP","NNS"]:
				token = extendedNERAnalyzedParse[key]["word"].lower()
				matched_cities = findCityByName(token)
				if matched_cities:
					"""if len(matched_cities) == 1:
						matched_city_name = matched_cities[0][1]
						matched_city_token = matched_city_name.split()
						for w in matched_city_token:
							if w == token:
								fl = matched_cities[0][0]
								extendedNERAnalyzedParse[key]['NER'] = cityMarker
								extendedNERAnalyzedParse[key]['NormalizedNER'] = matched_cities[0][1]
					else:"""
					for city in matched_cities:
						matched_flag = 1
						city_name_list = city[1].split()
						if len(city_name_list) == 1 and city_name_list[0].lower() == token:
							fl.append(city[0])
							extendedNERAnalyzedParse[key]['NER'] = cityMarker
							extendedNERAnalyzedParse[key]['NormalizedNER'] = city[1]
							cityTokens.append((key,key+1,city[1]))
						else:
							for i in range(1,len(city_name_list)):
								if key+i>len(extendedNERAnalyzedParse) or extendedNERAnalyzedParse[key+i]["word"].lower() != city_name_list[i].lower():
									matched_flag = 0
							if matched_flag :
								cityTokens.append((key,key+len(city_name_list),city[1]))
								fl.append(city[0])
								extendedNERAnalyzedParse[key]['NER'] = cityMarker
								extendedNERAnalyzedParse[key]['NormalizedNER'] = city[1]
	except:
		logging.exception("error in findCity")
		cityTokens=[]
		fl=[]
		return fl,cityTokens
	return fl,cityTokens

	

def getLocalityList(locality_list):
	locality_token_list = []
	for item in locality_list:
		item_tokens = item[0].split()		# locality item contains spaces
		locality_token_list.append(item_tokens)
	return sorted(locality_token_list,key=len,reverse=True)

def matchLongestString(key,extendedNERAnalyzedParse,locality_list):
	locality_item_list = getLocalityList(locality_list)
	for item_tokens in locality_item_list:
		item_length = len(item_tokens)
		fl = 0
		for id in range(0,item_length):
			token_id = id + key
			if token_id >len(extendedNERAnalyzedParse):
				fl=1
				break
			word = extendedNERAnalyzedParse[token_id]['word'].lower()
			if not word == str(item_tokens[id]).lower():
				fl = 1
				break
		if fl == 0:
			return item_tokens, item_length
	return [],0

def inLocalityItemList(l,locality_index):
	start_l = l[0]
	end_l = l[1]
	for item in locality_index:
		start_item = item[0]
		end_item = item[1]

		if start_item<=start_l and end_item>=end_l:
			return True
	return False				    	
# load locality names from database, sets the value of NER and NormalizedNer of the fist word of the loaclity name
# requires city_id to identify the locality
# doesn;t return anything
def findLocality(extendedNERAnalyzedParse,city_id):
	matched_token_id = []
	matched_locality_item_list = []
	fl = 0
	matched = 0

	locality_item_list = []

	token_num = len(extendedNERAnalyzedParse)

	locality_index = []

	iterator = iter(range(1,token_num+1))
	try:
		for token_id in iterator:
			token = extendedNERAnalyzedParse[token_id]["word"]
			locality_item_list = findLocalityByName(city_id,token)
			matched_locality_item, item_length = matchLongestString(token_id,extendedNERAnalyzedParse,locality_item_list)
			if item_length > 0:
				l = [token_id,token_id+item_length]
				if not inLocalityItemList(l,locality_index):
					extendedNERAnalyzedParse[token_id]['NER'] = localityMarker
					extendedNERAnalyzedParse[token_id]['NormalizedNER'] = ' '.join(matched_locality_item)
					locality_index.append((l[0],l[1],' '.join(matched_locality_item)))
					matched = 1
					matched_locality_item_list.append(' '.join(matched_locality_item))
					#print token + " " + ' '.join(matched_locality_item)
		# print "locality",city_id, locality_index, matched_locality_item_list
	except:
		logging.exception("error in findLocality")
		locality_index=[]
		matched_locality_item_list=[]
		matched=0
		return locality_index, matched_locality_item_list, matched
	return locality_index, matched_locality_item_list, matched


'''
	for key in extendedNERAnalyzedParse.keys():   
		if extendedNERAnalyzedParse[key]["POS"] == "NN" or extendedNERAnalyzedParse[key]["POS"] == "NNP":
			token = extendedNERAnalyzedParse[key]["word"]
			matched_localities = findLocalityByName(city_id,token)
			if matched_localities:
				if len(matched_localities) == 1:
					matched_locality_name = matched_localities[0][1]
					matched_locality_token = matched_locality_name.split()
					for w in matched_locality_token:
						if w == token:
							fl = matched_localities[0][0]
					extendedNERAnalyzedParse[key]['NER'] = localityMarker			
					extendedNERAnalyzedParse[key]['NormalizedNER'] = matched_localities[0][1]
				elif matched_localities:
					for locality in matched_localities:
						matched_flag = 1
						locality_name_list = locality[1].split()
						if len(locality_name_list) == 1 :
							extendedNERAnalyzedParse[key]['NER'] = localityMarker			
							extendedNERAnalyzedParse[key]['NormalizedNER'] = locality[1]
							
						else:
							for i in range(1,len(locality_name_list)):
					    			if extendedNERAnalyzedParse[key+i]["word"] != locality_name_list[i]:
						    			matched_flag = 0
							if matched_flag :
								extendedNERAnalyzedParse[key]['NER'] = localityMarker			
								extendedNERAnalyzedParse[key]['normalizedNER'] = locality[1]
'''
			    	
'''
def existsLocality(extendedNERAnalyzedParse):
	identifiers = []
	with open(LOCALITY_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	
	identifierMatch = 0
	fl = 0
	for key in extendedNERAnalyzedParse.keys():
	    	token = extendedNERAnalyzedParse[key]["word"]
		for word in identifiers:	
			if(token == word): 		
				identifierMatch = 1
				fl = 1
				break
		if(fl == 1): 
			return 1			

def getLocality(extendedNERAnalyzedParse,city_name):
	    	
	localities = []
	LOCALITY_FILE = CITY_FOLDER + city_name + "/" + city_name + "_locality_list"
        with open(LOCALITY_FILE) as f:
        	for line in f:
	        	localities.append(line.rstrip())
	     
	locality_list = []
	for key in extendedNERAnalyzedParse.keys():
	    	token = extendedNERAnalyzedParse[key]["word"]
		for word in localities:	
			if(token == word):
				extendedNERAnalyzedParse[key]['NER'] = localityMarker			
				extendedNERAnalyzedParse[key]['NormalizedNER'] = locality			
				locality_list.append(token)
	if locality_list:
		return [city_name,locality_list]
'''
