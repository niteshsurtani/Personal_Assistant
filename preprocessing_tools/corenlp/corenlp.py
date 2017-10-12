import os
import subprocess
import NER_DOM_Parser
from subprocess import Popen, PIPE, STDOUT
import shlex
from number import *
import requests
from solveQueryForNumbers import solveNumber

def execute_java(stdin):
	parse = requests.post("http://0.0.0.0:4567/processQuery",data=stdin)
	text = parse.text
	return text

time_map = ['TAF','TMO','TNI','TEV']

def getDate(time_value):
	# Split at first T
	t = time_value.split('T')
	return t[0]

'''
TAF,TMO,TNI,TEV
'''
def updateTimeToDate(analyzedQuery):
	for parse in analyzedQuery:
		for key, value in parse.iteritems():
			if value["NER"] == "TIME":
				normalizedValue = value["NormalizedNER"]
				for time in time_map:
					if time in normalizedValue:
						date = getDate(normalizedValue)
						
						value["NER"] = "DATE"
						value["NormalizedNER"] = date
	return analyzedQuery

def identifyNER(query):
	'''
	(String) -> [Object], [String]

	Takes the input query and annotates Time and Number and return

	'''

	query = solveNumber(query)
	corenlp_time = execute_java(query)

	corenlp_number = annotateNumbers(query, corenlp_time)
	
	analyzedQuery,chunkedParse = outputToDict(corenlp_number)

	analyzedQuery = updateTimeToDate(analyzedQuery)
	return analyzedQuery, chunkedParse

def XmlToDict(xmlfile):
	elementsDict, chunkedParse = NER_DOM_Parser.convertXMLToDict(xmlfile)
	return elementsDict, chunkedParse

def outputToDict(file):
	elementsDict, chunkedParse = extractOutput(file)
	return elementsDict, chunkedParse

def extractOutput(output):
	parse = ""
	elementsDict = {}

	sentencesParse = []
	sentencesNER = []
	count = 0

	lines = output.split("\n")
	for line in lines:
		line = line.strip()
		if line[0:7] == "<parse>":
			parse = line[7:-1]
			sentencesParse.append(parse)
			sentencesNER.append(elementsDict)
			elementsDict = {}
		elif line.strip() != "":
			t = line.split()
			elementsDict[int(t[0])] = {}
			elementsDict[int(t[0])]["word"] = t[1]
			elementsDict[int(t[0])]["POS"] = t[2]
			elementsDict[int(t[0])]["lemma"] = t[3]
			elementsDict[int(t[0])]["NER"] = t[4]
			elementsDict[int(t[0])]["NormalizedNER"] = t[5]
		else:
			break
	return sentencesNER,sentencesParse
