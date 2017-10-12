from FILE_CONSTANTS import *
from operator import itemgetter

AMOUNT_EXIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/rules/amounts"
CURRENCY_LIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/rules/currency_list"
CURRENCY_DIRECTORY = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/rules/currency/"
VALUE_LIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/rules/value_list"
VALUE_DIRECTORY = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/rules/value/"
CSV_FILE_EXTENSION = ".csv"
amountMarker = "AMOUNT"

CATEGORIES_LIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/category/categories"
NEGATION = 'no'
PREP_LIST = ['to','-']
AND = 'and'
windowlength = 3
RANGE_WORD_LIST = ['between','range']

# AIM : To return tokenId of number terms
# input : extendedNERAnalyzedParse
# output : list of tokenId
def getNumberTokens(extendedNERAnalyzedParse):
    	numbertokenIdlist = []
	for key in extendedNERAnalyzedParse.keys():
	    	if extendedNERAnalyzedParse[key]["NER"] == "NUMBER":
		    	numbertokenIdlist.append(key)
	return numbertokenIdlist


# AIM : return a dictionary, keys = currency names(rupees), value = possible words for that currency(rs,RS,rupess)
# input : database file
# output : dictionary
def loadCurrencyList():
	currency_list = []
	with open(CURRENCY_LIST_FILE) as f:
		for line in f:
			currency_list.append(line.rstrip())
	f.close()

	currency_dict = {}
	for currency in currency_list:
		currency_dict[currency] = []
		fname = CURRENCY_DIRECTORY + currency + CSV_FILE_EXTENSION
		with open(fname) as f:
			for line in f:
				cur = line[:-1].split(",")
		f.close()
		currency_dict[currency] = cur
	return currency_dict

# AIM : return a dictionary, keys = value names(1000), value = possible words for that value(K, grand)
# input : database file
# output : dictionary
def loadValueList():
	value_list = []
	with open(VALUE_LIST_FILE) as f:
		for line in f:
			value_list.append(line.rstrip())
	f.close()

	value_dict = {}
	for value in value_list:
		
		value_dict[value] = []
		fname = VALUE_DIRECTORY + value + CSV_FILE_EXTENSION
	    
		with open(fname) as f:
			for line in f:
				val = line[:-1].split(",")
		f.close()
		value_dict[value] = val
	return value_dict

# AIM : find tokenId of number terms whose next word is a valueMarker 
# input : extendedNERAnalyzedParse, list of tokenId of number terms
# output : list of start and end tokenId of number term
def getValueMarkers(extendedNERAnalyzedParse, numbertokenIdlist):
	identifiers = []
	tokenAmt=[]
	with open(AMOUNT_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())

	value_dict = loadValueList()
	multiplier = 1
	value_flag = 0

	amount_terms = []

	for tokenId in numbertokenIdlist:
	    	valuemarkerId = tokenId + 1
		multiplier = 1
		value_flag = 0
		word = ''

		try:
	    		word = extendedNERAnalyzedParse[valuemarkerId]["word"].lower()
		except KeyError:
			    	pass
		if word in identifiers:
		    	for k in value_dict.keys():
				if word in value_dict[k]:
					multiplier = int(k[11:])
			#		print '***********'
			#		print multiplier	
					value_flag = 1
					
		if value_flag:
			if extendedNERAnalyzedParse[tokenId]["NormalizedNER"][0]  not in '0123456789':
				amount_term_string = extendedNERAnalyzedParse[tokenId]["NormalizedNER"][0] + str(float(extendedNERAnalyzedParse[tokenId]["NormalizedNER"][1:])*(multiplier))
			else:
				amount_term_string = str(float(extendedNERAnalyzedParse[tokenId]["NormalizedNER"])*(multiplier)) 
			#print tokenId
			#print amount_term_string
			#print value_flag
			extendedNERAnalyzedParse[tokenId]["NER"] = amountMarker
			extendedNERAnalyzedParse[tokenId]["NormalizedNER"] = amount_term_string
			amount_terms.append([amount_term_string,[tokenId,valuemarkerId]])
			tokenAmt.append((tokenId,valuemarkerId))
		else:
		    amount_terms.append(['',[tokenId,tokenId]])
	return amount_terms	,tokenAmt


# AIM : find tokenId of number terms whose next or previous word is a currency 
# input : extendedNERAnalyzedParse, list of start and end tokenId of number terms
# output : list of start and end tokenId of number term (currencyId, valueId, valuemarkerId)
def FindCurrency(extendedNERAnalyzedParse,amount_terms):
	identifiers = []
	with open(AMOUNT_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())

	currency_dict = loadCurrencyList()

	currency_term_list = []

	for amount_term_string,term in amount_terms:
		word1 = ''
		word2 = ''
		word = ''
		currency_tokenId = term[0]
		'''
	    	if len(term) == 1:
		    	try:
		    		word1 = extendedNERAnalyzedParse[term[0] + 1]["word"].lower()
			except KeyError:
			    	pass
			word2 = extendedNERAnalyzedParse[term[0] - 1]["word"].lower()
		'''
		if len(term) == 2:
		    	word1 = extendedNERAnalyzedParse[term[0] - 1]["word"].lower()
		    	try:
				word2 = extendedNERAnalyzedParse[term[1] + 1]["word"].lower()
			except KeyError:
			    	pass
		if word1 in identifiers:
			word = word1
			currency_tokenId = term[0] - 1
		elif word2 in identifiers:
			word = word2
			currency_tokenId = term[1] + 1
		for k in currency_dict.keys():
			if word in currency_dict[k]:
				extendedNERAnalyzedParse[term[0]]["NER"] = amountMarker
				extendedNERAnalyzedParse[term[0]]["NormalizedNER"] = k + ' ' + str(extendedNERAnalyzedParse[term[0]]["NormalizedNER"])
				#print  str(term[0]) + ', ' + str(extendedNERAnalyzedParse[term[0]]["NormalizedNER"])
		currency_term_list.append([currency_tokenId,term[0],term[1]])
	return currency_term_list

# AIM : check for range keywords within specified windowlength 
# input : extendedNERAnalyzedParse, windowlength and end tokenId
# output : 1 if present,  else 0
def CheckForRange(windowlength, extendedNERAnalyzedParse, endtoken):
    #    	print endtoken-windowlength, ' ' , endtoken
    	for key in range(endtoken-windowlength, endtoken):
		if extendedNERAnalyzedParse[key]["lemma"] in RANGE_WORD_LIST:
			return 1

# AIM : check for amount ranges
# input : extendedNERAnalyzedParse, list of start, end tokenId of number terms
# output : modifies NormalizedNER and NER for range number tokens 
def DetectRange(currency_term_list, extendedNERAnalyzedParse):
    	for index in range(1,len(currency_term_list)):
		if (currency_term_list[index][0] - currency_term_list[index-1][2]) == 2 :
		    #			print index,' ',index-1
		    	amt_flag = 0
			range_flag = 0
			if extendedNERAnalyzedParse[currency_term_list[index][0] - 1]["word"] == AND :
				if CheckForRange(windowlength, extendedNERAnalyzedParse, currency_term_list[index-1][0]):
				    	range_flag = 1
			
			if range_flag or extendedNERAnalyzedParse[currency_term_list[index][0] - 1]["word"] in PREP_LIST :
				if extendedNERAnalyzedParse[currency_term_list[index-1][1]]["NER"] == amountMarker or extendedNERAnalyzedParse[currency_term_list[index][1]]["NER"] == amountMarker:   	
					amt_flag = 1
				extendedNERAnalyzedParse[currency_term_list[index - 1][1]]["NormalizedNER"] = {"range": {"min":extendedNERAnalyzedParse[currency_term_list[index-1][1]]["NormalizedNER"], "max": extendedNERAnalyzedParse[currency_term_list[index][1]]["NormalizedNER"]},"exact" : ''}
				extendedNERAnalyzedParse[currency_term_list[index][1]]["NER"] = "O"
				if amt_flag :
				    extendedNERAnalyzedParse[currency_term_list[index-1][1]]["NER"] = amountMarker
		else:

		    if extendedNERAnalyzedParse[currency_term_list[index - 1][1]]["NER"] != "O":
		    	extendedNERAnalyzedParse[currency_term_list[index - 1][1]]["NormalizedNER"] = {"range": {"min":"", "max":"" },"exact" :extendedNERAnalyzedParse[currency_term_list[index - 1][1]]["NormalizedNER"] }
		    if index == len(currency_term_list) - 1:
			extendedNERAnalyzedParse[currency_term_list[index][1]]["NormalizedNER"] = {"range": {"min":"", "max":"" },"exact" :extendedNERAnalyzedParse[currency_term_list[index][1]]["NormalizedNER"]}
				
		    


# AIM : check for category keywords
# input : extendedNERAnalyzedParse, database file of categories
# output : list of tokenid of category key words and category [tokenId,category]
def GetCategoryKeyWords(extendedNERAnalyzedParse):
    	categories = {}
	with open(CATEGORIES_LIST_FILE) as f:
		for line in f:
			categories[line[:-1]] = []
			filename = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/category/" + line[:-1]
			with open(filename) as f2:
				for l in f2:
					categories[line[:-1]].append(l[:-1])
	
	
	matched_category = []
	for category in categories.keys():
		for keyword in categories[category]:
		    	keyword_list = keyword.split()
			matched_flag = 0
			for key in extendedNERAnalyzedParse.keys():
				if extendedNERAnalyzedParse[key]["lemma"].lower() == keyword_list[0]:
				    	matched_flag = 1
				    	if len(keyword_list) == 1 :
						matched_category.append([key,category])
						extendedNERAnalyzedParse[key]["NER"] = category
					else:
					    	length = len(keyword_list)
					    	for i in range(1,length):
							if extendedNERAnalyzedParse[key+1]["lemma"].lower() != keyword_list[i]:
								matched_flag = 0
								break
						if matched_flag:
						    	matched_category.append([key,category])
							extendedNERAnalyzedParse[key]["NER"] = category
	return matched_category


# AIM : checks for negation marker for categories
# input : extendedNERAnalyzedParse, categories detcted
# output : list of categories, tokenId and if value needed or not [tokenId, category, "yes"/"no"]
def FindNegationCategories(matched_category_list, extendedNERAnalyzedParse, chunkedParse):
    	matched_category_values = []
	parse = chunkedParse.split('(NP')
	amount_terms_count = 0
	for chunk in parse:
		chunk = chunk.replace('(','').replace(')','').lower()
		chunk = chunk.split()
		#print chunk
		for matched_category in matched_category_list:
			tokenId = matched_category[0]
			category = matched_category[1]
			if extendedNERAnalyzedParse[tokenId]['word'].lower() in chunk:
				if NEGATION in chunk:
				    #print chunk
					matched_category_values.append([tokenId,category,NEGATION])
				else:
				    	matched_category_values.append([tokenId,category,"yes"])
					amount_terms_count += 1
	return matched_category_values,amount_terms_count

# AIM : returns count of amount terms present
# input : extendedNERAnalyzedParse
# output : number of amount terms
def GetNumberofAmounts(extendedNERAnalyzedParse):
    	amount_count = 0
	amount_tokenId_list = []
    	for key in extendedNERAnalyzedParse.keys():
	    	if extendedNERAnalyzedParse[key]["NER"] == amountMarker:
			amount_count += 1
			amount_tokenId_list.append(key)
	return amount_tokenId_list, amount_count


# AIM : returns mapping of amount terms and categories
# input : extendedNERAnalyzedParse, matched cteagories tokenIds, list of start, end tokenId of number terms
# output : list of category and corresponding amount term
def Merge(matched_category_values,amount_tokenId_list, extendedNERAnalyzedParse):
	matched_category_values = sorted(matched_category_values, key=itemgetter(0))
	amount_tokenId_list = sorted(amount_tokenId_list)
	amount_index = 0
	for matched_category in matched_category_values:
	    #print '*****************'
		#print matched_category
	    	if matched_category[2] != NEGATION :
		    	matched_category[2] = extendedNERAnalyzedParse[amount_tokenId_list[amount_index]]['NormalizedNER']
			extendedNERAnalyzedParse[matched_category[0]]["NormalizedNER"] = matched_category[2]
			amount_index += 1
		else:
		    	extendedNERAnalyzedParse[matched_category[0]]["NormalizedNER"] = 0
	return matched_category_values


# AIM : returns a list of tokens with NER amount or number
# input : extendedNERAnalyzedParse
# output : list of tokenIds
def UpdateAmountList(extendedNERAnalyzedParse):
	amount_term_list = []
    	for key in extendedNERAnalyzedParse.keys():
	    	if extendedNERAnalyzedParse[key]['NER'] == 'NUMBER' or extendedNERAnalyzedParse[key]["NER"] == 'AMOUNT':
		    	amount_term_list.append(key)
	return amount_term_list

# AIM : returns mapping of amount terms and categories
# input : extendedNERAnalyzedParse, matched cteagories tokenIds, list of start, end tokenId of number terms
# output : list of category and corresponding amount term
def MergeNearest(matched_category_values,amount_tokenId_list,extendedNERAnalyzedParse):
    	for matched_category in matched_category_values:
	    	tokenId = matched_category[0]
		category = matched_category[1]
		if matched_category[2] != NEGATION:
		    	dist = 100
			matched_Id = -1
			for amount_tokenId in amount_tokenId_list:
			    if abs(int(tokenId) - int (amount_tokenId)) < dist :
					dist = abs(int(tokenId) - int (amount_tokenId))
					matched_Id = amount_tokenId
			matched_category[2] = extendedNERAnalyzedParse[matched_Id]["NormalizedNER"]
			extendedNERAnalyzedParse[matched_category[0]]["NormalizedNER"] = matched_category[2]
			amount_tokenId_list.remove(matched_Id)
		else:
		    	
			extendedNERAnalyzedParse[matched_category[0]]["NormalizedNER"] = 0
	return matched_category_values
