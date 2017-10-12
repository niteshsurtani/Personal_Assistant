from FILE_CONSTANTS import *
import logging

PREFERENCE_EXIST_FILE = EXTENDER_NER_DIRECTORY + "food/ner_rules/preference/preference_list"
preferenceMarker = "PREFERENCE"

def findPreference(extendedNERAnalyzedParse):
	
	identifiers = []
	tokenPref=[]
	with open(PREFERENCE_EXIST_FILE) as f:
		for line in f:
			identifiers.append(line.rstrip())
	
	identifierMatch = 0
	fl = 0
	matched_token_id = []
	preference_term = []
	try:
		for key in extendedNERAnalyzedParse.keys():
			token = extendedNERAnalyzedParse[key]["word"].lower()
			token_id = int(key)
			matched_flag = 0
			for preference in identifiers:
				preference_list = preference.split()
				length = len(preference_list)
				if extendedNERAnalyzedParse[token_id]['word'].lower() == preference_list[0]:
					matched_flag = 1
					if length == 1:
						fl = 1
						extendedNERAnalyzedParse[token_id]["NER"] = preferenceMarker
						extendedNERAnalyzedParse[token_id]["NormalizedNER"] = preference
						tokenPref.append((token_id,token_id+1,preference))
					for i in range(1,length):
						if preference_list[i] != extendedNERAnalyzedParse[token_id+i]['word'].lower():
							matched_flag = 0
							break
					if matched_flag :
						matched_token_id.append(range(token_id,token_id+length))
						matched_flag = 0
						tokenPref.append((token_id,token_id+length,preference))
						fl = 1
						extendedNERAnalyzedParse[token_id]["NER"] = preferenceMarker
						extendedNERAnalyzedParse[token_id]["NormalizedNER"] = preference
	except:
		logging.exception("error in findPreference")
		tokenPref=[]
		return tokenPref
	return tokenPref
	'''					
	for token_id in matched_token_id:
	    	preference_name = []
		for i in token_id:
			preference_name.append(extendedNERAnalyzedParse[i]['word'].lower())
		preference_term.append(preference_name)
	return matched_token_id,preference_term,fl
	'''


'''
def UpdatePreferenceNER(matched_token_id_list,preference_list,extendedNERAnalyzedParse):
    	preference_string_list = []
	for index,value in enumerate(preference_list):
	    	preference = ''
		for item in preference_list[index]:
		    	preference = preference + item + ' '
		preference_string_list.append(preference)
	for p in preference_string_list:
		if 'pure ' + p not in preference_string_list: 
			word_list = p.split()
			for key in extendedNERAnalyzedParse.keys():
	    			token = extendedNERAnalyzedParse[key]["word"].lower()
				if token == word_list[-1]:
	    				extendedNERAnalyzedParse[key]['NER'] = preferenceMarker 
					extendedNERAnalyzedParse[key]['NormalizedNER'] = p[:-1]
					print p[:-1]
'''	
