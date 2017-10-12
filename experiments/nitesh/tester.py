# Query: I want to buk a bos tikket from Hyderbad to Bangalore leaving on Tuesdy.
# Category: Travel_Bus
import os

query = "I want to book a 2AC ticket."
#query="I want to buk a flight tikket from new york to bangalore between 21st june and 23rd june."
category="travel"

import nltk
import spell_checker
import preprocess_output_parse

pwd=os.getcwd()
coreNLPDir=pwd+"/Tools/stanford-corenlp-full-2015-04-20"

#tokens = nltk.word_tokenize(query)
#print tokens

#correctly_spelled_words=spell_checker.spell_check(tokens)
#print correctly_spelled_words

#spell_checked_query=" ".join(correctly_spelled_words)+"\n";
#print "SPELL_CHECEKED "+spell_checked_query

##### TRUECASE CORRECTOR #######
# Change the class bias for Truecase Module
# Input: I want to book a flight ticket from new York to Bangalore between 21st June and 23rd June .
# Output: I want to book a flight ticket from New YORK TO BANGALORE between 21st June and 23rd June .

os.chdir(coreNLPDir)

truecaseFile = "truecase"
truecaseGeneratedFile = "truecase.xml"

truecaseTarget = open(truecaseFile, 'w')
#truecaseTarget.write("%s\n" %spell_checked_query)
truecaseTarget.write("%s\n" %query)
truecaseTarget.close()
os.system("java -cp '*' -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,truecase -file "+truecaseFile)
os.chdir(pwd)
truecaseQuery = preprocess_output_parse.TruecaseDOMParser(coreNLPDir,truecaseGeneratedFile)
print truecaseQuery
#################################

############# PRE-PROCESSING STEP #############
os.chdir(coreNLPDir)

targetFile = "pre_processing_input"
targetGeneratedFile = "pre_processing_input.xml"

target = open(targetFile, 'w')
#target.write("%s\n" %spell_checked_query)
target.write("%s\n" %query)
target.close()
os.system("java -cp '*' -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP [ props config ] -file "+targetFile)
os.chdir(pwd)

allLocations = preprocess_output_parse.PreProcessingDOMParser(coreNLPDir,targetGeneratedFile,"AllLocations")
for key, value in allLocations.iteritems():
	print key+" "+value

allDates = preprocess_output_parse.PreProcessingDOMParser(coreNLPDir,targetGeneratedFile,"AllDates")
for key, value in allDates.iteritems():
	print key+" "+value
################################################

################# IDENTIFYING OTHER MANDATORY AND OPTIONAL PARAMETERS #######################


#############################################################################################

############ LINKING LOCATION => SOURCE, DESTINATION AND DATE => START AND END DATE ######################


##########################################################################################################

# SEED LIST FOR IDENTIFYING THE SUB-CATEGORIES: TRANSACTION AND TRANSPORT

transactionList = ['book','cancel','status']
transportList = ['bus','train','flight']

# I want a flight from ....
# I want to book a flight ..
# Can you get me a ticket ...
# 

# I want to cancel my flight ...

# 
book = ['book','want','get']
cancel = ['cancel']
status = []

bus = ['bus']
train = ['train','railway']
flight = ['flight','aeroplane','air']

########################################################################


'''
words_pos=nltk.pos_tag(correctly_spelled_words)
print words_pos
'''
