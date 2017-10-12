from FILE_CONSTANTS import *
restaurantMarker = 'RESTAURANT'
from preprocessing_tools.extended_ner.food.api.restaurants import *
import re, logging
import copy

def getRestaurantList(restaurant_list):
	restaurant_token_list = []
	for item in restaurant_list:
		item_tokens = item[0].split()		# restaurant item contains spaces
		restaurant_token_list.append(item_tokens)
	return sorted(restaurant_token_list,key=len,reverse=True)

def matchLongestString(key,extendedNERAnalyzedParse,restaurant_list):
	restaurant_item_list = getRestaurantList(restaurant_list)
	for item_tokens in restaurant_item_list:
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

def inRestaurantItemList(l,restaurant_index):
	start_l = l[0]
	end_l = l[1]
	for item in restaurant_index:
		start_item = item[0]
		end_item = item[1]

		if start_item<=start_l and end_item>=end_l:
			return True
	return False

# load restaurant item list from database, marks NER and NormalizedNER values of the first word of the restaurant item
# doesn't return anything
def FindRestaurantItems(extendedNERAnalyzedParse):
	matched_token_id = []
	matched_restaurant_item_list = []
	fl = 0
	matched = 0

	restaurant_item_list = []

	token_num = len(extendedNERAnalyzedParse)

	restaurant_index = []

	try:
		iterator = iter(range(1,token_num+1))
		for token_id in iterator:
			if extendedNERAnalyzedParse[token_id]['POS'] in ["NN","NNP","NNS","JJ"]:
				#print "-*-"*50
				restaurant_item_list = findRestaurantByName(extendedNERAnalyzedParse[token_id]['word'])
				matched_restaurant_item, item_length = matchLongestString(token_id,extendedNERAnalyzedParse,restaurant_item_list)
				if item_length > 0:
					l = [token_id,token_id+item_length]
					if not inRestaurantItemList(l,restaurant_index):
						extendedNERAnalyzedParse[token_id]['NER'] = restaurantMarker
						extendedNERAnalyzedParse[token_id]['NormalizedNER'] = ' '.join(matched_restaurant_item)
						restaurant_index.append((l[0],l[1],' '.join(matched_restaurant_item)))
						matched = 1
						matched_restaurant_item_list.append(' '.join(matched_restaurant_item))
		# print matched_restaurant_item_list
	except:
		logging.exception("error in FindRestaurantItems")
		restaurant_index=[], matched_restaurant_item_list=[], matched=0
		return restaurant_index, matched_restaurant_item_list, matched
	return restaurant_index, matched_restaurant_item_list, matched
	'''
	## for debugging purposes
	for token_id in matched_token_id:
	    	restaurant_item = []
		for i in token_id:
			restaurant_item.append(extendedNERAnalyzedParse[i]['word'].lower())
		matched_restaurant_item.append(restaurant_item)
	return matched_token_id,matched_restaurant_item,fl
	'''
'''
1 large pizza
pizza 1 large
1 pizza large

500ml coke
coke 500ml cold

garlic bread 
cheese garlic bread
def UpdateRestaurantItemNER(matched_token_id_list,matched_restaurant_item_list,extendedNERAnalyzedParse):
	for index,value in enumerate(matched_restaurant_item_list):
	    	restaurant_item = ''
		for item in matched_restaurant_item_list[index]:
		    	restaurant_item = restaurant_item + item + ' '
		extendedNERAnalyzedParse[matched_token_id_list[index][-1]]['NER'] = restaurantMarker 
		extendedNERAnalyzedParse[matched_token_id_list[index][-1]]['NormalizedNER'] = restaurant_item[:-1]
		print restaurant_item[:-1]

'''
# parsed query broken into NP chunks, NP chunk further split by 'and', looks for matched restaurant item in the chunk
# and returns chunks with restaurant items, start and end token ids of chunk, the restaurant item matched and the matched restaurant item tokenId
def GetRestaurantItemChunks(matched_token_id_list,matched_restaurant_item_list,parse):
	restaurantChunks = []	
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
		for item in matched_restaurant_item_list:
			if item[0] in chunks[index].lower():
				if [word_list,start_token,end_token] not in chunk_list:
					chunk_list.append([word_list,start_token,end_token])
#	print matched_restaurant_item_list
	for index,tokenId in enumerate(matched_token_id_list):
		for ch,start,end in chunk_list:
		    #			print start, ' ', end, ' ', tokenId[0]
			if int(tokenId[0]) >= int(start) and int(tokenId[0]) <= int(end) :
			    #	print ch, ' ', tokenId[0],' ',matched_restaurant_item_list[index]
				restaurantChunks.append([ch,start,end,matched_restaurant_item_list[index],tokenId[0]])
				
#	print "restaurant chunks"
	return restaurantChunks
	
# look for numbers(quantity), volume, weight and adjectives(large,small,medium, cold) terms in chunks and returns list of the values
def GetQuantitySize(chunkList,extendedNERAnalyzedParse,matched_restaurant_item_list):
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
		restaurant_item = chunks[3]
		restaurant_tokenId = chunks[4]
	    	
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

		# print [restaurant_item,number_ner,pos_jj,weight_ner,volume_ner,size_ner]
		extendedNERAnalyzedParse[restaurant_tokenId]["NormalizedNER"] = [restaurant_item,number_ner,pos_jj,weight_ner,volume_ner,size_ner]
#		print restaurant_item
#		print number_ner
#		print pos_jj
#		print weight_ner
#		print volume_ner
#		print ''

							
							    

		
def GetQuantitySize1(extendedNERAnalyzedParse,matched_token_id_list):
	sequence=[]
	'''start=chunkList[0][1]
	end=chunkList[-1][2]'''
	# print matched_token_id_list
	start=1
	end=len(extendedNERAnalyzedParse)

	for tokenId in range(start,end+1):
		if extendedNERAnalyzedParse[tokenId]["NER"] == "VOLUME":
			sequence.append(("vol",tokenId))
		elif extendedNERAnalyzedParse[tokenId]["NER"] == "WEIGHT":
			sequence.append(("wt",tokenId))
		elif extendedNERAnalyzedParse[tokenId]["NER"] == "SIZE":
			sequence.append(("sz",tokenId))
		elif extendedNERAnalyzedParse[tokenId]["NER"] == "NUMBER":
			sequence.append(("qty", tokenId))
		elif extendedNERAnalyzedParse[tokenId]["NER"] == "FOOD":
			sequence.append(("food",tokenId))
		elif extendedNERAnalyzedParse[tokenId]["POS"] == "JJ":
			sequence.append(("adj",tokenId))
		elif extendedNERAnalyzedParse[tokenId]["word"] == ",":
			sequence.append(("delimit", tokenId))
		elif extendedNERAnalyzedParse[tokenId]["POS"] == "IN":
			sequence.append(("delimit",tokenId))
		elif extendedNERAnalyzedParse[tokenId]["POS"] == "CC":
			sequence.append(("delimit",tokenId))
	sequence.reverse()
	dic_food={}
	now={}
	fl=0
	curr_food=""
	now_fl=0
	try:
		for item in sequence:
			# print now
			# print dic_food
			if item[0] =="delimit" and fl==1:
				fl=0
				dic_food[curr_food]=copy.deepcopy(now)
				now={}
			elif item[0] in now and fl==1:
				fl=0
				dic_food[curr_food]=copy.deepcopy(now)
				now={}
				now[item[0]]=[item[1]]
			elif item[0]=="food" and fl==0:
				dic_food[item[1]]=now
				curr_food=item[1]
				fl=1
			elif item[0]=="food" and fl==1:
				dic_food[curr_food]=copy.deepcopy(now)
				now={}
				curr_food=item[1]
			else:
				now[item[0]]=[item[1]]
		if fl==1:
			dic_food[curr_food]=copy.deepcopy(now)
		# print dic_food
		for token in dic_food:
			extendedNERAnalyzedParse[token]["NormalizedNER"]=[]
			name=""
			for food_item in matched_token_id_list:
				if food_item[0]==token:
					for i in range(food_item[0],food_item[1]):
						if name:
							name+=" "+extendedNERAnalyzedParse[i]["word"]
						else:
							name+=extendedNERAnalyzedParse[i]["word"]
			extendedNERAnalyzedParse[token]["NormalizedNER"].append(name)
			for attribute in ["vol","wt","sz","qty"]:
				if attribute in dic_food[token]:
					extendedNERAnalyzedParse[token]["NormalizedNER"].append([extendedNERAnalyzedParse[dic_food[token][attribute][0]]["NormalizedNER"]])
				elif attribute=="qty":
					extendedNERAnalyzedParse[token]["NormalizedNER"].append([1])
				else:
					extendedNERAnalyzedParse[token]["NormalizedNER"].append([])
			if "adj" in dic_food[token]:
					extendedNERAnalyzedParse[token]["NormalizedNER"].append([extendedNERAnalyzedParse[dic_food[token]["adj"][0]]["word"]])
			else:
					extendedNERAnalyzedParse[token]["NormalizedNER"].append([])
	except:
		logging.exception("error in GetQuantitySize1")
		return
