import os
import sys
import nlp_preprocessing_engine
import filecmp

GOLD_DIRECTORY = "/testcases/nitesh/food/gold/"
OUTPUT_DIRECTORY = "/testcases/nitesh/food/output/"
XML_DIRECTORY = "/testcases/nitesh/food/xml/"

#home ="/home/urvashi/Desktop/Genie/genie_nlp/"
PWD = os.getcwd()
PREPROCESSING_TOOLS_DIRECTORY = "/preprocessing_tools/"
CORENLP_DIRECTORY = PWD+PREPROCESSING_TOOLS_DIRECTORY+"corenlp/"
CORENLP_GENERATED_FILE = CORENLP_DIRECTORY + "corenlp_input.xml"


def printDictionary(filename,directory,dictionary):
   	directory = PWD + directory
	target = open(directory+filename,'w')

	for key,value in dictionary.iteritems():
		if(isinstance(value,dict)):
			target.write(str(key)+"\t")
			for k1,v1 in value.iteritems():
					target.write(str(k1)+ " : "+str(v1)+",")
			target.write("\n")
		else:
			target.write(str(key) + " : " + str(value)+"\n")
	target.close()

fileName = PWD + "/testcases/nitesh/food/preprocessing_testcases"
queries = []
with open(fileName) as f:
	for line in f:
		if(len(line) > 0 and line[0]!='#'):
			queries.append(line)

# Changing google doc queries to required format
'''
count = 1
for queryLine in queries:
	queryLine = queryLine.rstrip()
	if(queryLine!="" and queryLine[0]!='#'):
		print str(count) + "\t" + queryLine
		count += 1
	else:
		print queryLine
'''

category = "food"
correct = 0
total = 1
incorrect = []
right = []
for queryLine in queries:
	queryLineList = queryLine.split('\t')
	query = queryLineList[0].rstrip()
	queryId = str(total)
	total += 1

#		if(int(queryId) > 10):
	preprocessingDF = nlp_preprocessing_engine.preprocessor(query,category)
	# First time to populate the output of the testcases and manually check them
	
	printDictionary(queryId,GOLD_DIRECTORY,preprocessingDF)
	#printDictionary(queryId,OUTPUT_DIRECTORY,preprocessingDF)
	XML_FILE = PWD + XML_DIRECTORY+queryId
	os.system("cp "+CORENLP_GENERATED_FILE+ " "+XML_FILE)

	'''
	XML_FILE = XML_DIRECTORY+queryId
	if(os.path.isfile(home+XML_FILE)):
		preprocessingDF = nlp_preprocessing_engine.preprocessor(query,category,home+XML_FILE)
	'''
	# To automatically match the output of the testcases
	#printDictionary(queryId,OUTPUT_DIRECTORY,preprocessingDF)
	# inputFile = GOLD_DIRECTORY + queryId
	# outputFile = OUTPUT_DIRECTORY + queryId
		
	'''
		if(os.path.isfile(inputFile) and os.path.isfile(outputFile)):
		if filecmp.cmp(inputFile,outputFile):
			right.append(queryId)
			correct += 1
		else:
			incorrect.append(queryId)
	'''
'''
print "Total " + correct + " testcases passed out of " + total
print "System failed on testcases with ID: "
print incorrect
'''
