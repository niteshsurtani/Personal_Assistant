import os
import nltk
import collections
# from mysql.connector import Error
import sys

import logging
import nlp_logging
from nlp_logging import logger

# Loads all the static variables to be used globally.
from FILE_CONSTANTS import *
from utilities.merge_dictionary import mergeDictionaries

import preprocessing_tools.noisy_word_normalizer.normalizer
import preprocessing_tools.number_string_splitter.number_string_splitter
import preprocessing_tools.abbreviation_checker.abbreviation_corrector
import preprocessing_tools.spell_checker.spell_checker
import preprocessing_tools.argument_filler.argument_filler
import preprocessing_tools.month_filler.month_filler
import preprocessing_tools.corenlp.corenlp
import preprocessing_tools.extended_ner.travel.travel_extended_ner
import preprocessing_tools.category_disambiguator.category_disambiguator
# import preprocessing_tools.extended_ner.food.food_extended_ner
# import preprocessing_tools.extended_ner.movie.movie_extended_ner


def preprocessor(query,category,last_requested_DF=""):
	'''
	(String,String,String) -> Object

	Takes the input query, category and last requested DF
	and routes it to corresponding category module.

	INPUT: ('hyd to blr', 'travel', 'source')
	OUTPUT: {source: HYD, destination: BLR}

	'''

	if category.lower() == "travel":
		return travelNLP(query,category,last_requested_DF)

	# elif category.lower() == "food":
	# 	return foodNLP(query,last_requested_DF)
	# elif category.lower() == "movie":
	# 	return movieNLP(query,category,last_requested_DF)


def travelNLP(query,category,last_requested_DF):
	'''
	(String,String,String) -> Object

	Takes the input query, category and last requested DF
	and annotates the NERs in the query.

	INPUT: ('hyd to blr', 'travel', 'source')
	OUTPUT: {source: HYD, destination: BLR}

	'''
	# logger = logging.getLogger(__name__)
	allExtendedNerDF = {}
	logger.info("ENTERING TRAVEL MODULE")

	try:
		logger.debug(query + " " + last_requested_DF + "\n" )

		query = query.lower()

		noiseRemovedQuery = preprocessing_tools.noisy_word_normalizer.normalizer.normalize(query)
		print "Normalize = ", noiseRemovedQuery
		logger.debug("Normalize = " + noiseRemovedQuery)


		splittedQuery = preprocessing_tools.number_string_splitter.number_string_splitter.splitNumberString(noiseRemovedQuery)
		print "Splitted = ", splittedQuery
		logger.debug("Splitted = " + splittedQuery)


		abbreviatedQuery = preprocessing_tools.abbreviation_checker.abbreviation_corrector.correctAbbreviation(splittedQuery)
		print "Abbreviated = ",abbreviatedQuery
		logger.debug("Abbreviated = " + abbreviatedQuery)


		spellCheckedQuery = preprocessing_tools.spell_checker.spell_checker.spellCheck(abbreviatedQuery,PWL_FILE)
		print "Spellchecked = ", spellCheckedQuery
		logger.debug("Spellchecked = " + spellCheckedQuery)


		monthFilledQuery = preprocessing_tools.month_filler.month_filler.completeDate(spellCheckedQuery)
		print "MonthFilledQuery = ", monthFilledQuery
		logger.debug("MonthFilledQuery = " + monthFilledQuery)


		gapFilledQuery = preprocessing_tools.argument_filler.argument_filler.fillArguments(monthFilledQuery)
		print "GapFilledQuery = ", gapFilledQuery
		logger.debug("GapFilledQuery = " + gapFilledQuery)
		

		normalizedQuery = gapFilledQuery
		print "Final Normalized Query = ", gapFilledQuery
		print
		logger.debug("Final Normalized Query = " + gapFilledQuery)


		NERAnalyzedParse, chunkedParse = preprocessing_tools.corenlp.corenlp.identifyNER(normalizedQuery)
		print "NER Parse = ", NERAnalyzedParse
		print "Chunking = ", chunkedParse

		for index in range(0,len(chunkedParse)):
			# print NERAnalyzedParse[index], chunkedParse[index]
			extendedNerDF = preprocessing_tools.extended_ner.travel.travel_extended_ner.identifyExtendedNER(normalizedQuery,category,NERAnalyzedParse[index],last_requested_DF)

			disambiguatedDF = preprocessing_tools.category_disambiguator.category_disambiguator.disambiguateCategories(normalizedQuery,category,NERAnalyzedParse[index],chunkedParse[index],last_requested_DF)
			# print "Disambiguated = ",
			# print disambiguatedDF

			singleExtendedNerDF = preprocessing_tools.category_disambiguator.category_disambiguator.mergeDictionaries(extendedNerDF,disambiguatedDF)
			allExtendedNerDF = mergeDictionaries(allExtendedNerDF,singleExtendedNerDF)
		
		if "0" in allExtendedNerDF.keys():
			del allExtendedNerDF["0"]

		print "Final Analyzed NERs = ", allExtendedNerDF

	except:
		# print "Unexpected error:", sys.exc_info()
		logger.error(sys.exc_info()[1])

	finally:
		logger.info("LEAVING TRAVEL MODULE")
		return allExtendedNerDF



# def foodNLP(query,last_requested_DF):
# 	allExtendedNerDF = {}
# 	query=query.lower()
# 	splittedQuery = preprocessing_tools.abbreviation_checker.number_string_splitter.number_string_splitter(query,RULES_DIRECTORY)
# 	print "Splitted Query = " + splittedQuery
# 	abbrQuery = ' '.join(preprocessing_tools.abbreviation_checker.abbr_corrector.abbr_detector(splittedQuery.split(),RULES_DIRECTORY,FILENAME))
# 	# print abbrQuery
# 	print "Abbreviated Query = " + abbrQuery
# 	#spellCheckedQuery = preprocessing_tools.spell_checker.spell_checker.spellCheck(abbrQuery,PWL_FILE,OTHER_WORDS_FILE)
# 	spellCheckedQuery=abbrQuery
# 	# print spellCheckedQuery
# 	print "Spell Checked = " + spellCheckedQuery

# 	truecaseQuery = spellCheckedQuery.lower()
# 	#truecaseQuery = preprocessing_tools.truecase.truecase.truecaseCorrector(TRUECASE_INPUT_FILE,TRUECASE_GENERATED_FILE,PWD,CORENLP_TOOL_DIRECTORY,spellCheckedQuery)
# 	#print "Truecase Output = " + truecaseQuery
# #	truecaseQuery = "I want to order 5 pizza from a restaurant with no delivery fee e Min order 100 and total cost between 1 K and RS 1200"

# 	NERAnalyzedParse, chunkedParse = preprocessing_tools.corenlp.corenlp.identifyNER(CORENLP_INPUT,CORENLP_GENERATED_FILE,PWD,CORENLP_DIRECTORY,CORENLP_TOOL_DIRECTORY,CONFIG_CORENLP,truecaseQuery)

# 	# print NERAnalyzedParse
# #	truecaseQuery = preprocessing_tools.truecase.truecase.truecaseCorrector(TRUECASE_INPUT_FILE,TRUECASE_GENERATED_FILE,PWD,CORENLP_TOOL_DIRECTORY,spellCheckedQuery)
# #	print "Truecase Output = " + truecaseQuery

# 	for index in range(0,len(chunkedParse)):
# 		entitiesList = preprocessing_tools.extended_ner.food.food_extended_ner.identifyExtendedNER(truecaseQuery,NERAnalyzedParse[index],chunkedParse[index])
# 		singleExtendedNerDF = preprocessing_tools.extended_ner.food.food_extended_ner.disambiguateTokens(NERAnalyzedParse[index],entitiesList)
# 		allExtendedNerDF = mergeDictionaries(allExtendedNerDF,singleExtendedNerDF)
	
# 	print
# 	print "=================================== ALL SENTENCE ANALYSIS PARSE =================================="
# 	print NERAnalyzedParse, chunkedParse
# 	print

# 	print allExtendedNerDF
# 	return dictToJSON(allExtendedNerDF)


# def movieNLP(query,category,last_requested_DF):
# 	allExtendedNerDF = {}
# 	query=query.lower()

# 	normalizedQuery = preprocessing_tools.normalizer.normalizer.normalize(query,WORDS_FILE)
# 	print "normalize = ", normalizedQuery

# 	splittedQuery = preprocessing_tools.abbreviation_checker.number_string_splitter.number_string_splitter(normalizedQuery,RULES_DIRECTORY)
# 	print "splitted", splittedQuery

# 	abbrQuery = ' '.join(preprocessing_tools.abbreviation_checker.abbr_corrector.abbr_detector(splittedQuery.split(),RULES_DIRECTORY,FILENAME))
# 	print "abbreviated query",abbrQuery

# 	spellCheckedQuery = preprocessing_tools.spell_checker.spell_checker.spellCheck(abbrQuery,PWL_FILE,OTHER_WORDS_FILE)
# 	print "spellchecked query", spellCheckedQuery

# 	# truecaseQuery = preprocessing_tools.truecase.truecase.truecaseCorrector(TRUECASE_INPUT_FILE,TRUECASE_GENERATED_FILE,PWD,CORENLP_TOOL_DIRECTORY,spellCheckedQuery)
# 	truecaseQuery = spellCheckedQuery.lower()
# 	truecaseQuery=abbrQuery.lower()

# 	NERAnalyzedParse, chunkedParse = preprocessing_tools.corenlp.corenlp.identifyNER(CORENLP_INPUT,CORENLP_GENERATED_FILE,PWD,CORENLP_DIRECTORY,CORENLP_TOOL_DIRECTORY,CONFIG_CORENLP,truecaseQuery)
# 	print NERAnalyzedParse

# 	for index in range(0,len(chunkedParse)):
# 		print NERAnalyzedParse[index], chunkedParse[index]
# 		extendedNerDF = preprocessing_tools.extended_ner.movie.movie_extended_ner.identifyExtendedNER(truecaseQuery,category,NERAnalyzedParse[index],last_requested_DF)
# 		# print "Extended = ",
# 		print extendedNerDF

# 		disambiguatedDF = preprocessing_tools.category_disambiguator.category_disambiguator.disambiguateCategories(truecaseQuery,category,NERAnalyzedParse[index],chunkedParse[index],last_requested_DF)
# 		# print "Disambiguated = ",
# 		# print disambiguatedDF

# 		singleExtendedNerDF = preprocessing_tools.category_disambiguator.category_disambiguator.mergeDictionaries(extendedNerDF,disambiguatedDF)
# 		allExtendedNerDF = mergeDictionaries(allExtendedNerDF,singleExtendedNerDF)
# 	print allExtendedNerDF
# 	# preprocessing_tools.category_disambiguator.category_disambiguator.printDictionary(preprocessingDF)
# 	if "0" in allExtendedNerDF.keys():
# 		del allExtendedNerDF["0"]
# 	return allExtendedNerDF

# def dictToJSON(dict):
# 	finalDict = {}
# 	attributeMultiple = ['FOOD','CUISINE','RESTAURANT']
# 	for key, val in dict.iteritems():
# 		if key.upper() in attributeMultiple:
# 			# Element is an array
# 			if key.upper() == "FOOD":
# 				finalDict[key.upper()] = []
				
# 				for food_item in val:
# 					foodDict = {}
# 					foodDict['QUANTITY'] = '1'
# 					foodDict['JJ'] = foodDict['WEIGHT'] = foodDict['VOLUME'] = foodDict['SIZE'] = ''
				
# 					finalDict[key.upper()].append(foodDict)

# 					foodDict['NAME'] = food_item[0]
					
# 					if len(food_item[1]) > 0:
# 						foodDict['VOLUME'] = food_item[1][0]

# 					if len(food_item[2]) > 0:
# 						foodDict['WEIGHT'] = food_item[2][0]

# 					if len(food_item[3]) > 0:
# 						foodDict['SIZE'] = food_item[3][0]
			
# 					if len(food_item[4]) > 0:
# 						foodDict['QUANTITY'] = food_item[4][0]
							
# 					if len(food_item[5]) > 0:
# 						foodDict['JJ'] = food_item[5][0]
					
# 			else:
# 				finalDict[key.upper()] = val
# 		else:
# 			if len(val) > 0:
# 				finalDict[key.upper()] = val[0]
# 			else:
# 				finalDict[key.upper()] = ""
# 	return finalDict

