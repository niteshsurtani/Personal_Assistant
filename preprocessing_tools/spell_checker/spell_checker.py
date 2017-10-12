import nltk
import enchant
import sys
import re
from nltk.metrics import edit_distance

import logging
import nlp_logging
from nlp_logging import logger

from preprocessing_tools.noisy_word_normalizer.spell_normalizer import normalize


class SpellingReplacer(object):
	'''
	Initializes the spell checker instance of
	Enchant and Personalized Word List (PWL)
	'''

	def __init__(self, dict_name = 'en_US', max_dist = 2):
		if dict_name == 'en_US':
			self.spell_dict = enchant.Dict(dict_name)
		else:
			self.spell_dict = enchant.request_pwl_dict(dict_name)			
		self.max_dist = 2

	def check(self, word):
		if self.spell_dict.check(word):
			return 1
		return 0

	def replace(self, word):
		suggestions = self.spell_dict.suggest(word)
		if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
			return suggestions[0]
		else:
			return word

def spellCheck(query,PWLFile):
	unigram_spelled_query = unigramSpellCheck(query,PWLFile)
	return unigram_spelled_query

def unigramSpellCheck(query,PWLdict):
	'''
	(String) -> String

	Takes a noisy query with ungrammatical/Out of Vocab words as
	input and returns the spell corrected query.

	INPUT: I want to buk a flight from hydrabad to banglore.
	OUTPUT: I want to book a flight from Hyderabad to Bangalore.

	'''

	logger.info("ENTERING SPELL CHECKER MODULE")

	try:
		logger.debug("Query = " + query)

		word_list = nltk.word_tokenize(query)
		pos_list = nltk.pos_tag(word_list)

		replacerDict = SpellingReplacer()
		# print replacerDict.check("mumbai")

		replacerPWL = SpellingReplacer(PWLdict)
		# print replacerPWL.check('mumbai')

		checked_list = []
		for item in pos_list:
			word = item[0]
			pos = item[1]

			truncate_word = re.sub(r'(.)\1+', r'\1', word)
			normalized_word = normalize(truncate_word)

			# If word is a special char, don't spell check it
			if re.match("([^\w@#])",word):
				checked_list.append(word)
				
			elif normalized_word:
				checked_list.append(normalized_word)
				
			elif replacerPWL.check(truncate_word):
				correctedWord = truncate_word.title()
				checked_list.append(correctedWord)

			elif not replacerDict.check(word):
				correctedWord = ""
				dist = 100

				# Do not replace words from PWL if len(word) <= 3
				if len(truncate_word) > 3:
					correctedWordPWL = replacerPWL.replace(truncate_word)
					distPWL = edit_distance(truncate_word, correctedWordPWL)
				else:
					distPWL = dist
					correctedWordPWL = truncate_word

				correctedWordDict = replacerDict.replace(word)
				distDict = edit_distance(word, correctedWordDict)

				if distPWL > distDict or correctedWordPWL == truncate_word:
					correctedWord = correctedWordDict
				else:
					correctedWord = correctedWordPWL.title()
				
				if correctedWord == "":
					correctedWord = word
				else:
					logger.debug("'%s' --> '%s' ", word, correctedWord)
		
				checked_list.append(correctedWord)
			else:
				checked_list.append(word)

		spell_checked_query = " ".join(checked_list);
		
		logger.info("SPELL CORRECTION DONE\n")
		return spell_checked_query

	except:
		logger.error(sys.exc_info()[1])
		logger.info("SPELL CORRECTION DONE\n")
		return query
