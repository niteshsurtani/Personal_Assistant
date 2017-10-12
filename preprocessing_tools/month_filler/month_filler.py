import sys
import re
import datetime
from datetime import date

import logging
import nlp_logging
from nlp_logging import logger

from utilities.match_longest_string import *
from utilities.check_type import isNumber, isDateToken

month_list = []
for i in range(1,13):
    month_list.append(datetime.date(1990, i, 1).strftime('%B'))


def isMonthSpecified(index,tokens):
	try:
		start_index = index - 2
		if start_index < 0:
			start_index = 0

		end_index = index + 3
		if end_index > len(tokens):
			end_index = len(tokens)

		for i in range(start_index, end_index):
			token = tokens[i]
			if token in month_list:
				return True
		return False
	except:
		logger.error(sys.exc_info()[1])
		return False

# def isRelativeMonthSpecified(index,tokens):
# 	start_index = index - 2
# 	if start_index < 0:
# 		start_index = 0

# 	end_index = index + 3
# 	if end_index > len(tokens):
# 		end_index = len(tokens)

# 	skip_tokens = []
# 	month = ''
# 	for i in range(start_index, end_index):
# 		token = tokens[i]

# 		matched_phrase = getMonthPhrase(token)
# 		for phrase_tuple in matched_phrase:
# 			phrase = phrase_tuple[0]
# 			offset = phrase_tuple[1]
# 			if matchLongestStringQuery(tokens,index,phrase):
# 				month = getMonthFromOffset(offset)

# 				phrase_tokens = phrase.split()
# 				phrase_length = len(phrase_tokens)
# 				skip_tokens = range(i,i+phrase_length)
# 				return skip_tokens, month
# 	return skip_tokens, month

def getComingMonth(given_date):
	try:
		today = date.today()
		today_date = today.day
		month = today.month

		if given_date <= today_date:
			month += 1
			month %= 12

		monthstr = datetime.date(1900, month, 1).strftime('%B')
		return monthstr
	except:
		logger.error(sys.exc_info()[1])
		return ''

def completeDate(query):
	'''
	(String) -> String

	Takes a query with incomplete dates (missing month), and fills it
	using Server Time. Also, it replaces 'th' to make the term number
	for gap filling module.

	INPUT: I will be travelling on 25th.
	OUTPUT: I will be travelling on 25 October.

	'''

	logger.info("ENTERING GAP FILLER MODULE")
	
	try:
		logger.debug("Query = " + query)

		gap_filled_query = ""

		tokens = query.split()
		new_tokens = []

		skip_flag = 0
		skip_tokens = []

		for index in range(0,len(tokens)):
			token = tokens[index]
			date = isDateToken(token)
			if date:
				new_tokens.append(str(date))
				if not isMonthSpecified(index,tokens):
					month = getComingMonth(date)
					new_tokens.append(month)
				# else:
				# 	skip_tokens, month = isRelativeMonthSpecified(index,tokens)
				# 	if skip_tokens:
				# 		new_tokens.append(month)
				# 		skip_flag = 1
			else:
				# if skip_flag and index not in skip_tokens:
				# 	skip_flag = 0
				# 	skip_tokens = []
				# if not skip_flag:
				new_tokens.append(token)

		gap_filled_query = " ".join(new_tokens)

		logger.info("GAP FILLING DONE\n")
		return gap_filled_query
	
	except:
		logger.error(sys.exc_info()[1])
		logger.info("GAP FILLING DONE\n")
		return query
