# Query: I want to buk a bos tikket from Hyderbad to Bangalore leaving on Tuesdy.
# Category: Travel_Bus
import os

#query = "I want to book a 2AC ticket."
#query="I want to buk a flight tikket from new york to bangalore between 21st june and 23rd june."
query="I want a bus on 27th aug."

import nltk
import spell_checker

tokens = nltk.word_tokenize(query)
#print tokens

correctly_spelled_words=spell_checker.spell_check(tokens)
#print correctly_spelled_words

spell_checked_query=" ".join(correctly_spelled_words)+"\n";
print "SPELL_CHECEKED "+spell_checked_query
