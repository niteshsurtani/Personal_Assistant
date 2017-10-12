from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *
from PATH_CONSTANTS import *

from preprocessing_tools.extended_ner.travel.api.stops import *
from utilities.match_longest_string import *

import re
import logging
import nlp_logging
from nlp_logging import logger

import datetime
from datetime import date, timedelta

time_NER = ['duration','date']
timeUnit = "hour"


def isNumber(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def calculateTime(unit, amount):
	hour_per_day = 24
	minutes_per_hour = 60

	if unit == "D":
		return hour_per_day * amount
	elif unit == "H":
		return amount
	elif unit == "M":
		return amount * 1.0 / minutes_per_hour

def calculateDate(tokens, addWeek):
	week_date = date(int(tokens[0]),int(tokens[1]),int(tokens[2]))
	new_date = week_date + datetime.timedelta(days=addWeek*7)
	return new_date

def normalizeTime(extendedNERAnalyzedParse):
	'''
	(Object) -> Object

	Takes the NER Parse as input and converts Stanford SUTime
	duration and date convention to our convention.

	INPUT: PT2H, 2015-09-28-WXX-1
	OUTPUT: 2, 2015-10-05

	'''

	logger.info("ENTERING TIME NORMALIZATION IDENTIFICATION MODULE")

	for key in extendedNERAnalyzedParse.keys():   
		ner = extendedNERAnalyzedParse[key]["NER"].lower()
		normalizedValue = extendedNERAnalyzedParse[key]["NormalizedNER"]
	
		if ner in time_NER:
			if ner == "duration":
				value = ""
				range_dict = {"exact":"","range":{"min":"","max":""}}

				normalizedValue = re.sub("\>|\<",r"",normalizedValue)
				if normalizedValue[0:2] == "PT":
					value = normalizedValue[-2:]
				elif normalizedValue[0:1] == "P":
					value = normalizedValue[1:]

				unit = value[-1:]
				amount = value[0:-1]

				if isNumber(amount):
					amount = int(amount)
					hours = calculateTime(unit, amount)

					range_dict["exact"] = hours

					extendedNERAnalyzedParse[key]["NormalizedNER"] = range_dict

			elif ner == "date":

				tokens = normalizedValue.split("-")
				length_token = len(tokens)
				
				if length_token >= 3 and tokens[2][0:2] == "WE":
					print "Weekend Identified"
				
				elif length_token > 4 and tokens[3][0:1] == "W":
					offset = tokens[4]
					addWeek = 0

					if isNumber(offset):
						offset = int(offset)

						today = datetime.datetime.today().weekday() + 1
						if today > offset:
							addWeek = 1

						week_date = calculateDate(tokens, addWeek)

						extendedNERAnalyzedParse[key]["NormalizedNER"] = week_date.strftime("%Y-%m-%d")


	logger.info("TIME NORMALIZATION DONE")
