import os
import truecase_DOM_parser


##### TRUECASE CORRECTOR #######
# Change the class bias for Truecase Module
# Input: I want to book a flight ticket from new York to Bangalore between 21st June and 23rd June .
# Output: I want to book a flight ticket from New YORK TO BANGALORE between 21st June and 23rd June .
def truecaseCorrector(inputFile,outputFile,PWD,CORENLP_DIRECTORY,query):
	os.chdir(CORENLP_DIRECTORY)

	target = open(inputFile, 'w')
	target.write("%s\n" %query)
	target.close()
	os.system("java -cp '*' -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,truecase -file "+inputFile)
	os.chdir(PWD)
	
	truecaseQuery = truecase_DOM_parser.TruecaseDOMParse(CORENLP_DIRECTORY,outputFile)
	return truecaseQuery

