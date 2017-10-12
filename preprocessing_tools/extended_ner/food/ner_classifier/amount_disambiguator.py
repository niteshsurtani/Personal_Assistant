'''
in all check for 'no' in same NP chunk
1) check for 'minimum order'
2) check for 'delivery' + 'fee/cost/charges/amount'
3) check for 'budget/cost/price/spend'

return tokenids


1) get number of amounts
2) 
3) one one mapping

'''
from FILE_CONSTANTS import *
amountMarker = "AMOUNT"
CATEGORIES_LIST_FILE = EXTENDER_NER_DIRECTORY + "ner_rules/amount/category/categories"
negationMarker = "no"

def GetNumberofAmounts(extendedNERAnalyzedParse):
    	amount_count = 0
	amount_tokenId_list = []
    	for key in extendedNERAnalyzedParse.keys():
	    	if extendedNERAnalyzedParse[key]["NER"] == amountMarker:
			amount_count += 1
			amount_tokenId_list.append(key)
	return amount_count,amount_tokenId_list

def GetKeyWords(extendedNERAnalyzedParse):
    	categories = {}
	with open(CATEGORIES_LIST_FILE) as f:
		for line in f:
			categories[line[:-1]] = []
			filename = EXTENDER_NER_DIRECTORY + "ner_rules/amount/category/" + line[:-1]
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
						matched_category.append([key,category,keyword_list])
					else:
					    	length = len(keyword_list)
					    	for i in range(1,length):
							if extendedNERAnalyzedParse[key+1]["lemma"].lower() != keyword_list[i]:
								matched_flag = 0
								break
						if matched_flag:
						    	matched_category.append([key,category,keyword_list])
	return matched_category


					
				

			
		   	

	
		    	
