import nltk
import enchant
import re
from nltk.metrics import edit_distance
class SpellingReplacer(object):
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

replacerDict = SpellingReplacer()
f = open("c","r")
for line in f:
	abr = line.strip()
	if replacerDict.check(abr):
		print abr

