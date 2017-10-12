from FILE_CONSTANTS import *

AMOUNT_EXIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/rules/amounts"
CURRENCY_LIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/rules/currency_list"
CURRENCY_DIRECTORY = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/rules/currency/"
VALUE_LIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/rules/value_list"
VALUE_DIRECTORY = EXTENDER_NER_DIRECTORY + "food/ner_rules/amount/rules/value/"
CSV_FILE_EXTENSION = ".csv"
amountMarker = "AMOUNT"

def existsAmount(extendedNERAnalyzedParse):
	
	identifiers = []
	with open(AMOUNT_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	
	identifierMatch = 0
	fl = 0
	for key in extendedNERAnalyzedParse.keys():
	    	token = extendedNERAnalyzedParse[key]["word"].lower()
		for word in identifiers:	
			if(token == word): 		
				identifierMatch = 1
				fl = 1
				break
		if(fl == 1): 
			return 1			

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

def getAmounts(extendedNERAnalyzedParse):
	identifiers = []
	with open(AMOUNT_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	f.close()

	currency_dict = loadCurrencyList()
	value_dict = loadValueList()
	
	value_flag = 0	
	currency_flag = 0
	amount_terms = []
	amounts = []
	multiplier = 1

	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		word = tokenInfoDict["word"].lower()
		if word in identifiers:
			tokenId = key
			value_flag = 0 	
			for k in value_dict.keys():
				if word in value_dict[k]:
					multiplier = int(k[11:])
		    			value_flag = 1
			# Dont give a test case like Rs. 10,000 as it is splitted into two sentences
			if value_flag:
			    	# print "value"
				if(extendedNERAnalyzedParse[tokenId-1]["NER"] == "NUMBER"): 
					valueId = tokenId -1
				else:
					valueId = tokenId + 1
			
				if extendedNERAnalyzedParse[valueId]["NormalizedNER"][0]  not in '0123456789':
				    amount_term_string = extendedNERAnalyzedParse[valueId]["NormalizedNER"][0] + str(float(extendedNERAnalyzedParse[valueId]["NormalizedNER"][1:])*(multiplier))
				else:
				    amount_term_string = str(float(extendedNERAnalyzedParse[valueId]["NormalizedNER"])*(multiplier)) 
				# print amount_term_string
				# print value_flag
				extendedNERAnalyzedParse[valueId]["NER"] = amountMarker
				extendedNERAnalyzedParse[valueId]["NormalizedNER"] = amount_term_string
			#	extendedNERAnalyzedParse[tokenId]["NormalizedNER"] = amount_term_string
				amount_terms.append([amount_term_string,[valueId,tokenId]])
	
	for amount_term_string,tokenIdlist in amount_terms:
		for k in currency_dict.keys():
		    #	    		for valueId,tokenId in tokenIdlist:
		    		valueId = tokenIdlist[0] 
				tokenId = tokenIdlist[1]
		    		word1 = extendedNERAnalyzedParse[valueId-1]["word"].lower()
				word2 =  extendedNERAnalyzedParse[tokenId+1]["word"].lower()
				if word1 in currency_dict[k]:
					currency_name = k
					currency_flag = 1
					amount_term_string = currency_name + ' ' + amount_term_string 
					extendedNERAnalyzedParse[valueId]["NER"] = amountMarker
					extendedNERAnalyzedParse[valueId]["NormalizedNER"] = amount_term_string
					amounts.append(amount_term_string)
					# print amount_term_string
					break
				elif word2 in currency_dict[k]:
					currency_name = k
					currency_flag = 1
					amount_term_string = currency_name + ' ' + amount_term_string 
					extendedNERAnalyzedParse[valueId]["NER"] = amountMarker
					extendedNERAnalyzedParse[valueId]["NormalizedNER"] = amount_term_string
					# print amount_term_string
					amounts.append(amount_term_string)
					# print amounts
					break
	    	
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
			word = tokenInfoDict["word"].lower()
			if word in identifiers:
				tokenId = key
				currency_flag = 0
				for k in currency_dict.keys():
					if word in currency_dict[k]:
						currency_name = k
						currency_flag = 1
				if currency_flag :
					if(extendedNERAnalyzedParse[tokenId-1]["NER"] == "NUMBER"): 
					    	# print "-"
						valueId = tokenId -1
					else:
					    	# print "+"
						valueId = tokenId + 1
					# print valueId
					try :
						amount_term_string = currency_name + ' ' + str(float(extendedNERAnalyzedParse[valueId]["NormalizedNER"])) 
						extendedNERAnalyzedParse[valueId]["NER"] = amountMarker
						extendedNERAnalyzedParse[valueId]["NormalizedNER"] = amount_term_string
						amounts.append(amount_term_string)
						# print amounts
					except KeyError:
					    	# print "here"
					    	continue
						
		
	return amounts	
	'''
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		word = tokenInfoDict["word"].lower()
		if word in identifiers:
			tokenId = key
			currency_flag = 0
			for k in currency_dict.keys():
				if word in currency_dict[k]:
					currency_name = k
					currency_flag = 1
			if currency_flag :
				if(extendedNERAnalyzedParse[tokenId-1]["NER"] == "NUMBER"): 
					valueId = tokenId -1
				else:
					valueId = tokenId + 1
				amount_term_string = currency_name + ' ' + str(float(extendedNERAnalyzedParse[valueId]["NormalizedNER"])) 
				extendedNERAnalyzedParse[tokenId]["NER"] = amountMarker
				extendedNERAnalyzedParse[tokenId]["NormalizedNER"] = amount_term_string
		
				amount_terms.append(amount_term_string)
	'''


