from FILE_CONSTANTS import *
import logging

# CUISINE_EXIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/cuisine/cuisine_list"
cuisineMarker = "CUISINE"
from preprocessing_tools.extended_ner.food.api.cuisine import *
# look  for cuisine terms in the query and marks NER to CUISINE
def findCuisine(extendedNERAnalyzedParse):
    #   	print findAllCuisines()
	identifiers = findAllCuisines()

	identifierMatch = 0
	fl = 0
	matched_token_id = []
	cuisine_list = []
	try:
		for key in extendedNERAnalyzedParse.keys():
			token = extendedNERAnalyzedParse[key]["word"].lower()
			token_id = int(key)
			matched_flag = 0
			for cuisine in identifiers:
				cuisine_name_list = cuisine.split()
				# print cuisine_name_list
				length = len(cuisine_name_list)
				if extendedNERAnalyzedParse[token_id]['word'].lower() == cuisine_name_list[0]:
					matched_flag = 1
					if length == 1:
						fl = 1
						extendedNERAnalyzedParse[token_id]['NER'] = cuisineMarker
						extendedNERAnalyzedParse[key]['NormalizedNER'] = cuisine
					for i in range(1,length):
						if cuisine_name_list[i] != extendedNERAnalyzedParse[token_id+i]['word'].lower():
							matched_flag = 0
							break
					if matched_flag :
						matched_token_id.append((token_id,token_id+length,cuisine))
						matched_flag = 0
						fl = 1
						extendedNERAnalyzedParse[token_id]['NER'] = cuisineMarker
						extendedNERAnalyzedParse[key]['NormalizedNER'] = cuisine
	except:
		matched_token_id = []
		cuisine_list=[]
		fl=0
		logging.exception("some error in 'findCuisine'")
		return matched_token_id,cuisine_list,fl
	for token_id in matched_token_id:
		cuisine_name = []
		for i in range(token_id[0],token_id[1]):
			cuisine_name.append(extendedNERAnalyzedParse[i]['word'].lower())
		cuisine_list.append(cuisine_name)
	return matched_token_id,cuisine_list,fl



'''
def UpdateCuisineNER(matched_token_id_list,cuisine_list,extendedNERAnalyzedParse):
	for index,value in enumerate(cuisine_list):
	    	cuisine = ''
		for item in cuisine_list[index]:
		    	cuisine = cuisine + item + ' '
		extendedNERAnalyzedParse[matched_token_id_list[index][-1]]['NER'] = cuisineMarker 
		extendedNERAnalyzedParse[matched_token_id_list[index][-1]]['NormalizedNER'] = cuisine[:-1]
		print cuisine[:-1]
'''
