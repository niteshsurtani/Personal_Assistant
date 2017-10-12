import os
import nltk
import re

from xml.dom import minidom

from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *
from PATH_CONSTANTS import *
# Returns whether the query has CLASS information or not. If NO information of class, then the class
# identification module is not processed further.

def existsAmount(query):
	tokens = nltk.word_tokenize(query)
	
	identifiers = []
	with open(AMOUNT_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	
	identifierMatch = 0
	fl = 0
	for word in identifiers:
		for token in tokens:
				token = token.lower()
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

def checkAmountWithoutUnit(extendedNERAnalyzedParse):
	print "========== AMOUNT CODE ======"
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		word = tokenInfoDict["word"].lower()
		ner = tokenInfoDict["NER"]
		normalizedValue = tokenInfoDict["NormalizedNER"]
		
		if ner == "NUMBER" and int(normalizedValue) > 100:
			extendedNERAnalyzedParse[key]["NER"] = amountMarker

def getAmounts(extendedNERAnalyzedParse):
	identifiers = []
	with open(AMOUNT_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	f.close()

	currency_dict = loadCurrencyList()
	value_dict = loadValueList()
	
	amount_terms = []
	multiplier = 1
	currency_name = "rupees"
	
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		word = tokenInfoDict["word"].lower()
		ner = tokenInfoDict["NER"]
		normalizedValue = tokenInfoDict["NormalizedNER"]

		if word in identifiers:
			tokenId = key

			for k in currency_dict.keys():
				if word in currency_dict[k]:
					currency_name = k
				
			for k in value_dict.keys():
				if word in value_dict[k]:
					multiplier = int(k[11:])
			
			# Dont give a test case like Rs. 10,000 as it is splitted into two sentences
			prev_id = tokenId-1
			next_id = tokenId+1
			if(prev_id in extendedNERAnalyzedParse and extendedNERAnalyzedParse[prev_id]["NER"] == "NUMBER"):
				valueId = tokenId - 1
			else:
				valueId = tokenId + 1

			amount_term_string = str(float(extendedNERAnalyzedParse[valueId]["NormalizedNER"])*(multiplier)) 

			extendedNERAnalyzedParse[valueId]["NER"] = amountMarker			
			extendedNERAnalyzedParse[valueId]["NormalizedNER"] = amount_term_string
			extendedNERAnalyzedParse[tokenId]["NER"] = amountMarker			
			extendedNERAnalyzedParse[tokenId]["NormalizedNER"] = amount_term_string
			amount_terms.append(amount_term_string)


	return amount_terms	


