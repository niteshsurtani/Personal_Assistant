from FILE_CONSTANTS import *
from preprocessing_tools.extended_ner.travel.api.range_handler import *
from utilities.match_longest_string import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *

import logging
import nlp_logging
from nlp_logging import logger

import unicodedata
import datetime
from datetime import date, timedelta

AROUND_PERCENT = 20.0

RANGE_NER = ['PRICE_RANGE','NUM_SEATS','NUM_STOPS','TIME_PREFERENCE','DATE','EXTRA_LUGGAGE','DURATION']
INTEGER_NER = ['NUM_SEATS','NUM_STOPS','EXTRA_LUGGAGE']
FLOAT_NER = ['PRICE_RANGE','TIME_PREFERENCE','DURATION']
DATE_NER = ['DATE']

def higherAround(value, AROUND_PERCENT):
	return value + ( AROUND_PERCENT * 1.0 / 100 ) * value

def lowerAround(value, AROUND_PERCENT):
	return value - ( AROUND_PERCENT * 1.0 / 100 ) * value

def addDays(given_date, num_days):
	d = given_date + datetime.timedelta(days=num_days)
	return d.strftime("%Y-%m-%d")

def subtractDays(given_date, num_days):
	new_date = given_date - datetime.timedelta(days=num_days)
	today = date.today()
	if new_date < today:
		new_date = today
	return new_date.strftime("%Y-%m-%d")

def setNormalizedValueDict(extendedNERAnalyzedParse,ner_key,normalizedValue):
	given_ner = extendedNERAnalyzedParse[ner_key]['NER']
	parse_length = len(extendedNERAnalyzedParse) + 1

	for key in range(ner_key,parse_length):
		ner = extendedNERAnalyzedParse[key]['NER']
		if ner == given_ner:
			extendedNERAnalyzedParse[key]['NormalizedNER'] = normalizedValue
		else:
			break
	return extendedNERAnalyzedParse

def convertToRange(extendedNERAnalyzedParse, ner_key, range_category):
	ner_token = extendedNERAnalyzedParse[ner_key]['NER']
	if ner_token in RANGE_NER:
		NER_values = getNERSemantics(ner_token)


		if NER_values:
			minimum = str(NER_values[0])
			maximum = str(NER_values[1])
			
			normalizedValueDict = extendedNERAnalyzedParse[ner_key]['NormalizedNER']
			if not isinstance(normalizedValueDict, dict):
				if isinstance(normalizedValueDict, unicode):
					val = unicodedata.normalize('NFKD', normalizedValueDict).encode('ascii','ignore')
				else:
					val = normalizedValueDict
				normalizedValueDict = {"exact":val, "range":{"min":"","max":""}}

			normalizedValue = normalizedValueDict['exact']

			if ner_token in INTEGER_NER:

				normalizedValue = int(normalizedValue)
				if range_category == 'AROUND':
					normalizedValueDict['range']['min'] = higherAround(normalizedValue, AROUND_PERCENT)
					normalizedValueDict['range']['max'] = lowerAround(normalizedValue, AROUND_PERCENT)

				elif range_category == 'LESS':
					normalizedValueDict['range']['min'] = minimum
					normalizedValueDict['range']['max'] = normalizedValue

				elif range_category == 'MORE':
					normalizedValueDict['range']['min'] = normalizedValue
					normalizedValueDict['range']['max'] = maximum


			elif ner_token in FLOAT_NER:

				normalizedValue = float(normalizedValue)
				print "normalizedValue"
				print normalizedValue
				if range_category == 'AROUND':
					normalizedValueDict['range']['min'] = higherAround(normalizedValue, AROUND_PERCENT)
					normalizedValueDict['range']['max'] = lowerAround(normalizedValue, AROUND_PERCENT)

				elif range_category == 'LESS':
					normalizedValueDict['range']['min'] = minimum
					normalizedValueDict['range']['max'] = normalizedValue

				elif range_category == 'MORE':
					normalizedValueDict['range']['min'] = normalizedValue
					normalizedValueDict['range']['max'] = maximum


			elif ner_token in DATE_NER:
				date_val = normalizedValue.split("-")
				given_date = date(int(date_val[0]), int(date_val[1]), int(date_val[2]))
				maximum = int(maximum)

				if range_category == 'AROUND':
					normalizedValueDict['range']['min'] = subtractDays(given_date, maximum/2)
					normalizedValueDict['range']['max'] = addDays(given_date, maximum/2)

				elif range_category == 'LESS':
					normalizedValueDict['range']['min'] = subtractDays(given_date, maximum)
					normalizedValueDict['range']['max'] = given_date.strftime("%Y-%m-%d")

				elif range_category == 'MORE':
					normalizedValueDict['range']['min'] = given_date.strftime("%Y-%m-%d")
					normalizedValueDict['range']['max'] = addDays(given_date, maximum)
			
	
			normalizedValueDict['exact'] = ""
		
			extendedNERAnalyzedParse = setNormalizedValueDict(extendedNERAnalyzedParse,ner_key,normalizedValueDict)
			return extendedNERAnalyzedParse

		else:
			return extendedNERAnalyzedParse

	else:
		return extendedNERAnalyzedParse

def updateRangeInNER(extendedNERAnalyzedParse):
	'''
	(Object) -> Object

	Takes the NER Parse as input and updates the values of NERs which are marked as
	exact but are actually range values, eg. before 27th October.

	INPUT: less than Rs 10,000, around 4 p.m., mumbai
	OUTPUT: {"exact":null, "range":{"max":10000,"min":0}}, {"exact":null, "range":{"max":16,"min":0}}, no

	'''

	logger.info("ENTERING RANGE HANDLER MODULE")


	# print "================ ENTeRED NER HERE =================="
	# print extendedNERAnalyzedParse
	print "===================================================="
	for key in extendedNERAnalyzedParse.keys():   
		token = extendedNERAnalyzedParse[key]["word"]
		matched_range_identifiers = getRangeIdentifier(token)
		for range_identifier in matched_range_identifiers:
			word = range_identifier[0]
			category = range_identifier[1]

			if matchLongestString(extendedNERAnalyzedParse,key,word):
				# Get NER key => where identifier ends
				word_length = len(word.split())
				ner_key = key + word_length
				if ner_key in extendedNERAnalyzedParse.keys():
					ner_token = extendedNERAnalyzedParse[ner_key]['NER']
					if ner_token != "0":
						convertToRange(extendedNERAnalyzedParse, ner_key, category)

						print "Range Identified = " + ner_token + " " + category
						# logger.debug("City Identified = '%s' with code = '%s'", city, city_code)
	# print "================ LEAVING NER HERE =================="
	# print extendedNERAnalyzedParse
	print "===================================================="
	logger.info("RANGE HANDLER DONE")
