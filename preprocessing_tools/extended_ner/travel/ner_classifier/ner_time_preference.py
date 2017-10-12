from FILE_CONSTANTS import *
from preprocessing_tools.extended_ner.travel.api.time_preference import *
from utilities.match_longest_string import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *

import datetime
import logging
import nlp_logging
from nlp_logging import logger

time_format = '%H:%M'
seconds_in_hour = 3600
hours_in_day = 24


def calculateTime(start_time,end_time,start_percent,end_percent):
	if start_time > end_time:
		end_time += hours_in_day

	# Apply  y = mx + c equation
	m = end_time - start_time
	start_m = start_percent * m / 100.0
	end_m = end_percent * m / 100.0

	new_start_time = start_time + start_m
	new_end_time = start_time + end_m
	return new_start_time, new_end_time

def getTimePreference(extendedNERAnalyzedParse):
	'''
	(Object) -> Object

	Takes the NER Parse as input and annotates the semantic time periods like morning, late evening.

	INPUT: late evening, afternoon, mumbai
	OUTPUT: yes, yes, no

	'''

	logger.info("ENTERING TIME PREFERENCE MODULE")

	for key in extendedNERAnalyzedParse.keys():   
		token = extendedNERAnalyzedParse[key]["word"]
		matched_period = getTimePeriod(token)
		if matched_period:
			time_preference = {"exact":"", "range":{"min":"", "max": ""}}

			start_time = matched_period[0].seconds*1.0/seconds_in_hour
			end_time = matched_period[1].seconds*1.0/seconds_in_hour

			previous_key = key - 1
			match_modifier = ()
			if previous_key in extendedNERAnalyzedParse:
				previous_token = extendedNERAnalyzedParse[previous_key]["word"]
				match_modifier = isTimeModifier(previous_token)

			# New time ranges
			if match_modifier:
				# Calculate new time period
				start_percent = match_modifier[0]
				end_percent = match_modifier[1]
				start_time, end_time = calculateTime(start_time,end_time,start_percent,end_percent)
			
			time_preference["range"]["min"] = start_time
			time_preference["range"]["max"] = end_time
			extendedNERAnalyzedParse[key]["NER"] = timePreferenceMarker
			extendedNERAnalyzedParse[key]["NormalizedNER"] = time_preference
			logger.debug("Time Preference Identified between %.2f and %.2f", start_time, end_time)

	logger.info("TIME PREFERENCE DONE")
