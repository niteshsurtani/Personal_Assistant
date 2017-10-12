import nltk
import enchant
import re
from pprint import pprint
from collections import OrderedDict
from operator import itemgetter
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

def asort(d):
     return sorted(d.items(), key=lambda x: x[1], reverse=True)

f1 = open("test","w")
f2 = open("train","w")

replacerDict = SpellingReplacer()
f = open("dish","r")
dict = {}
for line in f:
	line = line.strip()
	item = line.split()
	if len(item) > 1:
		c = item[0]
		word = item[1]
		if not replacerDict.check(word):
			word = re.sub(r'(.)\1+', r'\1', word) 
			if word not in dict.keys():
				dict[word] = int(c)
			else:
				dict[word] += int(c)

finalDictWord = {}
pwlWord = {}

d = OrderedDict(sorted(dict.items(), key=itemgetter(1)))
for key, val in d.iteritems():
	if int(val) > 4:
		f2.write(key+"\n")
		finalDictWord[key] = int(val)
	else:
		pwlWord[key] = int(val)
		
PWLdict = "train"
replacerPWL = SpellingReplacer(PWLdict)

for word in pwlWord.keys():
	correctWord = replacerPWL.replace(word)
	if correctWord in finalDictWord:
		finalDictWord[correctWord] += pwlWord[word]
	else:
		finalDictWord[correctWord] = pwlWord[word]

for word in finalDictWord.keys():
	print word

