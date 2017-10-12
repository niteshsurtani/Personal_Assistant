from FILE_CONSTANTS import *
foodMarker = 'FOOD'
from preprocessing_tools.extended_ner.food.api.menu import *
#from preprocessing_tools.extended_ner.food.temp_api.foodpanda_menu import *
import re, logging

def getFoodList(food_list):
	food_token_list = []
	for item in food_list:
		item_tokens = item[0].split()		# food item contains spaces
		food_token_list.append(item_tokens)
	return sorted(food_token_list,key=len,reverse=True)

def matchLongestString(key,extendedNERAnalyzedParse,food_list):
	food_item_list = getFoodList(food_list)
	for item_tokens in food_item_list:
		item_length = len(item_tokens)
		fl = 0
		for id in range(0,item_length):
			token_id = id + key
			if token_id > len(extendedNERAnalyzedParse):
				#print item_tokens
				fl=1
				break
			word = extendedNERAnalyzedParse[token_id]['word'].lower()
			if not word == str(item_tokens[id]).lower():
				fl = 1
				break
		if fl == 0:
			return item_tokens, item_length
	return [],0

def inFoodItemList(l,food_index):
	start_l = l[0]
	end_l = l[1]
	for item in food_index:
		start_item = item[0]
		end_item = item[1]

		if start_item<=start_l and end_item>=end_l:
			return True
	return False

# load food item list from database, marks NER and NormalizedNER values of the first word of the food item
# doesn't return anything
def FindFoodItems(query,extendedNERAnalyzedParse):
	matched_token_id = []
	matched_food_item_list = []
	fl = 0
	matched = 0

	food_item_list = []

	token_num = len(extendedNERAnalyzedParse)

	food_index = []


	try:
		iterator = iter(range(1,token_num+1))
		for token_id in iterator:
			if extendedNERAnalyzedParse[token_id]['POS'] in ["NN","NNP","NNS","JJ"]:
				food_item_list = findDishByName(extendedNERAnalyzedParse[token_id]['word'])
				if extendedNERAnalyzedParse[token_id]['word']=="pizza":
					print "*"*10,food_item_list
				matched_food_item, item_length = matchLongestString(token_id,extendedNERAnalyzedParse,food_item_list)
				if item_length > 0:
					l = [token_id,token_id+item_length]
					if not inFoodItemList(l,food_index):
						for i in range(token_id,token_id+item_length):
							extendedNERAnalyzedParse[i]['NER'] = "0"
						extendedNERAnalyzedParse[token_id]['NER'] = foodMarker
						extendedNERAnalyzedParse[token_id]['NormalizedNER'] = ' '.join(matched_food_item)
						food_index.append([l[0],l[1],' '.join(matched_food_item)])
						matched = 1
						matched_food_item_list.append(' '.join(matched_food_item))
	except:
		logging.exception("error in FindFoodItems")
		matched_food_item_list=[]
		food_index=[]
		matched=[]
		return food_index, matched_food_item_list, matched
	return food_index, matched_food_item_list, matched
	'''
	## for debugging purposes
	for token_id in matched_token_id:
	    	food_item = []
		for i in token_id:
			food_item.append(extendedNERAnalyzedParse[i]['word'].lower())
		matched_food_item.append(food_item)
	return matched_token_id,matched_food_item,fl
	'''
'''
1 large pizza
pizza 1 large
1 pizza large

500ml coke
coke 500ml cold

garlic bread 
cheese garlic bread
def UpdateFoodItemNER(matched_token_id_list,matched_food_item_list,extendedNERAnalyzedParse):
	for index,value in enumerate(matched_food_item_list):
	    	food_item = ''
		for item in matched_food_item_list[index]:
		    	food_item = food_item + item + ' '
		extendedNERAnalyzedParse[matched_token_id_list[index][-1]]['NER'] = foodMarker 
		extendedNERAnalyzedParse[matched_token_id_list[index][-1]]['NormalizedNER'] = food_item[:-1]
		print food_item[:-1]

'''
# parsed query broken into NP chunks, NP chunk further split by 'and', looks for matched food item in the chunk
# and returns chunks with food items, start and end token ids of chunk, the food item matched and the matched food item tokenId
def GetFoodItemChunks(matched_token_id_list,matched_food_item_list,parse):
	print parse
	foodChunks = []	
	NPChunks = parse.split('(NP')
	token_count = 0
	start_token = 0
	end_token = -1
	chunk_list = []
	for npchunk in NPChunks:
	    chunks =  npchunk.split('and)')
	    for index,chunk in enumerate(chunks) :
	    	start_token = end_token + 1
	    	chunk = chunks[index].split()
		word_list = []
		for word in chunk:
		    	word = word.strip()
			if word[0] != '(' :
			    	token_count += 1
				word_list.append(word.rstrip(')'))
		end_token = token_count
		for item in matched_food_item_list:
			if item[0] in chunks[index].lower():
				if [word_list,start_token,end_token] not in chunk_list:
					chunk_list.append([word_list,start_token,end_token])
#	print matched_food_item_list
	for index,tokenId in enumerate(matched_token_id_list):
		for ch,start,end in chunk_list:
		    #			print start, ' ', end, ' ', tokenId[0]
			if int(tokenId[0]) >= int(start) and int(tokenId[0]) <= int(end) :
			    #	print ch, ' ', tokenId[0],' ',matched_food_item_list[index]
				foodChunks.append([ch,start,end,matched_food_item_list[index],tokenId[0]])
				
#	print "food chunks"
	return foodChunks
	
# look for numbers(quantity), volume, weight and adjectives(large,small,medium, cold) terms in chunks and returns list of the values
def GetQuantitySize(chunkList,extendedNERAnalyzedParse,matched_food_item_list):
    #   	print "chunklist "," ", chunkList
	for chunks in chunkList:
		    	
	    	number_ner = []
		volume_ner = []
		weight_ner = []
		size_ner = []
		pos_jj = []
		chunk = chunks[0]
#		print chunk
		start = chunks[1]
		end = chunks[2]
		food_item = chunks[3]
		food_tokenId = chunks[4]
	    	
		for tokenId in range(start,end+1):
		    	if extendedNERAnalyzedParse[tokenId]["NER"] == "VOLUME":
			    	volume_ner.append(extendedNERAnalyzedParse[tokenId]["NormalizedNER"])
			elif extendedNERAnalyzedParse[tokenId]["NER"] == "WEIGHT":
			    	weight_ner.append(extendedNERAnalyzedParse[tokenId]["NormalizedNER"])
			elif extendedNERAnalyzedParse[tokenId]["NER"] == "SIZE":
			    	size_ner.append(extendedNERAnalyzedParse[tokenId]["NormalizedNER"])
			elif extendedNERAnalyzedParse[tokenId]["NER"] == "NUMBER":
			    	number_ner.append(extendedNERAnalyzedParse[tokenId]["NormalizedNER"])
				extendedNERAnalyzedParse[tokenId]["NER"] = "QUANTITY"
			elif extendedNERAnalyzedParse[tokenId]["POS"] == "JJ":
			    	pos_jj.append(extendedNERAnalyzedParse[tokenId]["word"])

		print [food_item,number_ner,pos_jj,weight_ner,volume_ner,size_ner]
		extendedNERAnalyzedParse[food_tokenId]["NormalizedNER"] = [food_item,number_ner,pos_jj,weight_ner,volume_ner,size_ner]
#		print food_item
#		print number_ner
#		print pos_jj
#		print weight_ner
#		print volume_ner
#		print ''

							
							    

		
