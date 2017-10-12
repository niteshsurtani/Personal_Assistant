from FILE_CONSTANTS import *

PAYMENT_MODE_EXIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/paymentmode/payment_mode"
paymodeMarker = "PAYMENT MODE"

def findPaymentMode(extendedNERAnalyzedParse):
    	identifiers = {}
	with open(PAYMENT_MODE_EXIST_FILE) as f:
		for line in f:
			identifiers[line[:-1]] = []
			filename = EXTENDER_NER_DIRECTORY + "food/ner_rules/paymentmode/" + line[:-1]
			with open(filename) as f2:
				for l in f2:
					identifiers[line[:-1]].append(l[:-1])

	identifierMatch = 0
	fl = 0
	matched_token_id = []
	for key in extendedNERAnalyzedParse.keys():
		tokenPay=[]
	    	token = extendedNERAnalyzedParse[key]["word"].lower()
		token_id = int(key)
		matched_flag = 0
		for paymode_list in identifiers.keys():
		    for paymode in identifiers[paymode_list]:
			paymode_name_list = paymode.split()
			length = len(paymode_name_list)
			if extendedNERAnalyzedParse[token_id]['word'].lower() == paymode_name_list[0].lower():
				matched_flag = 1
				if length == 1:
				    	fl = 1
				    	extendedNERAnalyzedParse[token_id]['NER'] = paymodeMarker
					extendedNERAnalyzedParse[key]['NormalizedNER'] = paymode_list
					tokenPay.append([key,key+1,paymode_list])
				for i in range(1,length):
					if paymode_name_list[i] != extendedNERAnalyzedParse[token_id+i]['word'].lower():
					 	matched_flag = 0
					   	break
				if matched_flag :
					matched_token_id.append(range(token_id,token_id+length))
					tokenPay.append([token_id,token_id+length,paymode_list])
					matched_flag = 0
					fl = 1
				    	extendedNERAnalyzedParse[token_id]['NER'] = paymodeMarker
					extendedNERAnalyzedParse[key]['NormalizedNER'] = paymode_list
	return tokenPay
