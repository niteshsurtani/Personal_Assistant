import os
import nltk
import re

from PATH_CONSTANTS import *


	
def normalizeParse(extendedNERAnalyzedParse):
	fl = 0
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		if(tokenInfoDict["NER"] == "DATE" and fl == 0):
			fl = 1
		elif(tokenInfoDict["NER"] == "DATE" and fl == 1):
			tokenInfoDict["NER"] = "0"
			tokenInfoDict["NormalizedNER"] = "0"
		else:
			fl = 0
	return extendedNERAnalyzedParse

def getNumberOfDates(NERAnalyzedParse,chunkedParse):
	
	dateList = {}	
	rangeIdentifiers = loadSeedlist(DISAMBIGUATOR_DATE_RANGE_PREPOSITIONS)
	# Return tokens of dates that are in range
	NERAnalyzedParse = normalizeParse(NERAnalyzedParse)
	
	rangeDateKeys = getRangeDates(rangeIdentifiers,NERAnalyzedParse,dateList,chunkedParse)
	# print "List ============ "
	# print dateList

	# All other dates are exact dates
	getExactDates(NERAnalyzedParse,dateList,rangeDateKeys)
	# print "List ============ "
	# print dateList
	return dateList


def loadSeedlist(fileName):
	seedlist = []
	with open(fileName) as f:
		line = f.readline().strip()
		seedlist = line.split(",")
	return seedlist

def getRangeDates(rangeIdentifiers,NERAnalyzedParse,dateList,chunkedParse):
	dateKeys = []
	for key,tokenInfoDict in NERAnalyzedParse.iteritems():
		for word in rangeIdentifiers:
			if(tokenInfoDict["word"] == word):
				# Check if next NNP is Date
				if(isNextNPDate(key,NERAnalyzedParse,chunkedParse)):
					# Pick next two dates as range
					rangeDates = getNextTwoRangeDates(key,NERAnalyzedParse,dateKeys)
					# Simple comparison of dates
					dateListLength = len(dateList)


					dateRange = {"range":{'min':"",'max':""},"exact":""}
					dateList[dateListLength] = dateRange
					if(rangeDates[0] < rangeDates[1]):
						dateList[dateListLength]['range']['min'] = rangeDates[0]
						dateList[dateListLength]['range']['max'] = rangeDates[1]
					else:
						dateList[dateListLength]['range']['min'] = rangeDates[1]
						dateList[dateListLength]['range']['max'] = rangeDates[0]
	return dateKeys		

def getNextTwoRangeDates(key,NERAnalyzedParse,dateKeys):
	dateList = []
	count = 0
	parseLength = len(NERAnalyzedParse)

	dateFlag = 0
	for index in range(key+1,parseLength+1):
		if(NERAnalyzedParse[index]["NER"] == "DATE"):
			if(dateFlag == 0):
				dateFlag = 1
				date = NERAnalyzedParse[index]["NormalizedNER"]
		else:
			if(dateFlag == 1):
				dateList.append(date)
				dateKeys.append(index-1)
				count += 1
				if(count == 2):
					break
			dateFlag = 0
	return dateList

def getNextNPChunkKeys(key,chunkedParse):
	# Reaching key token
	count = 0
	chunk_start = 0
	chunk_end = 0

	matchedIndex = 0
	tokens = chunkedParse.split()
	tokens_size = len(tokens)

	for index in range(0,tokens_size):
		token = tokens[index]
		if (token[0]!='('):
			count += 1;
			if(count == key):
				matchedIndex = index
				break
		# Find next NP chunk
	in_brak = 0
	start = 0 # Start matching the in_brak when first NP matched

	flag = 0
	for index in range(matchedIndex+1, tokens_size):
		token = tokens[index]
		if(start == 1 and token[0] == '('):
			in_brak += 1

		elif(start == 1 and token[len(token)-1] == ')'):
			# If token[0] == ')', it is considered as a word and not parse ).
			for i in range(1,len(token)):
				if(token[i] == ')'):
					in_brak -= 1
					if(in_brak == 0):
						flag = 1						
						chunk_end = index
						break

		if(start == 0 and token in ("(NP","(NP-TMP")):
			if(tokens[index + 1] in ("(NP","(NP-TMP")):
				continue

			chunk_start = index
			start = 1
			in_brak += 1
		
		if(flag == 1):
			break

	# Map chunk_start, chunk_end to token index
	token_start = 1
	token_end = 1
	count = 0
	mapper = 0
	flag = 0

	for index in range(0,tokens_size):
		token = tokens[index]
		if (token[0]!='('):
			mapper += 1;
			if(flag == 0 and count >= chunk_start):
				token_start = mapper
				flag = 1

			elif(flag == 1 and count >= chunk_end):
				token_end = mapper
				break
		count += 1
	return token_start, token_end


def isNextNPDate(key,NERAnalyzedParse,chunkedParse):
	chunk_start, chunk_end = getNextNPChunkKeys(key,chunkedParse)
	# print "Chunk = ",
	# print chunk_start, chunk_end
	parseLength = len(NERAnalyzedParse)
	for index in range(chunk_start,chunk_end+1):
		if(NERAnalyzedParse[index]["NER"] == "DATE"):
			return 1
		else:
			return 0

def getExactDates(NERAnalyzedParse,dateList,dateKeys):

	for key,tokenInfoDict in NERAnalyzedParse.iteritems():
		if(tokenInfoDict["NER"] == "DATE"):
			if key not in dateKeys:
				dateListLength = len(dateList)
				if type(tokenInfoDict["NormalizedNER"]) == dict:
					dateList[dateListLength] = tokenInfoDict["NormalizedNER"]
				else:
					dateRange = {"range":"","exact":""}
					dateList[dateListLength] = dateRange
					dateList[dateListLength]['exact'] = tokenInfoDict["NormalizedNER"]

def disambiguateDates(dateList,numDates,chunkedParse):
	dateDF = {}
	if(numDates == 2):
		dateComparison = []
		if(dateList[0]['exact'] == ""):
			dateComparison.append(dateList[0]['range']['min'])
		else:
			dateComparison.append(dateList[0]['exact'])

		if(dateList[1]['exact'] == ""):
			dateComparison.append(dateList[1]['range']['min'])
		else:
			dateComparison.append(dateList[1]['exact'])

		if (dateComparison[0] <= dateComparison[1]):
			dateDF['start_date'] = dateList[0]
			dateDF['end_date'] = dateList[1]
		else:
			dateDF['start_date'] = dateList[1]
			dateDF['end_date'] = dateList[0]
		return dateDF
'''
	elif(numDates == 1):

		start_date = ""
		end_date = ""
		
		prepositionChunkList = getDatePPChunks(dateList,chunkedParse)
		print prepositionChunkList
		for chunk in prepositionChunkList:
			prep = extractPrepositionFromChunk(chunk)
			date = extractDateFromChunk(chunk)

			if(checkPrepositionSource(prep)):
				start_date = date
				dateDF["start_date"] = start_date
			elif(checkPrepositionDestination(prep)):
				end_date = date
				dateDF["end_date"] = end_date

		if(len(dateDF) == numDates):
	#		print "Rule 1 applied"
			return dateDF


		# Step 2. If no information from step 1, then use verbs 
		verbInflected = ""
		verbChunkList = getDateVPChunks(dateList,chunkedParse)
	#	print "Chunk List"
	#	print verbChunkList
		for chunk in verbChunkList:
			verbInflected = extractVerbFromChunk(chunk)
			if(verbInflected != ""):
				verbInflected = verbInflected.lower()
			verb = extractRootForm(verbInflected,extendedNERAnalyzedParse)
	#		print "Root verb form = " + verb
			date = extractDateFromChunk(chunk)
	#		print "Date = "+date
			if(checkVerbSource(verb)):
				start_date = date
				dateDF["start_date"] = start_date
			elif(checkVerbDestination(verb)):
				end_date = date
				dateDF["end_date"] = end_date
				
		if(len(dateDF) == numDates):
	#		print "Rule 2 applied"
			return dateDF


		# Step 3. If no verb matched, find SOURCE and DESTINATION keywords in the query.
		start_datePosition = 0
		end_datePosition = 0

		start_datePosition = findSourcePosition(extendedNERAnalyzedParse,DISAMBIGUATOR_DATE_SOURCE_KEYWORDS)
		end_datePosition = findDestinationPosition(extendedNERAnalyzedParse,DISAMBIGUATOR_DATE_DESTINATION_KEYWORDS)

		if(start_datePosition !=0  and end_datePosition != 0):
			if(start_datePosition < end_datePosition):
				start_date = dateList[0]
				end_date = dateList[1]
				dateDF["start_date"] = start_date
				dateDF["end_date"] = end_date
			else:
				start_date = dateList[1]
				end_date = dateList[0]
				dateDF["start_date"] = start_date
				dateDF["end_date"] = end_date
		elif(start_datePosition !=0  and end_datePosition == 0):
			# Pick date from dateList not in dateDF['end_date']
			if(numDates == 1):
				dateDF["start_date"] = dateList[0]
			elif(numDates == 2):
				dateDestination = dateDF["end_date"]
				for loc in dateList:
					if(loc!=dateDestination):
						start_date = loc
						dateDF["start_date"] = start_date
		elif(start_datePosition ==0  and end_datePosition != 0):
			if(numDates == 1):
				dateDF["end_date"] = dateList[0]
			elif(numDates == 2):
				dateSource = dateDF["start_date"]
				for loc in dateList:
					if(loc!=dateSource):
						end_date = loc
						dateDF["end_date"] = end_date
		if(len(dateDF) == numDates):
	#		print "Rule 3 applied"
			return dateDF
		
		# Step 4. Treat first date as Source and second date as Destination.
		if(len(dateDF) == 1):
			if(start_date == ""):
				dateDestination = dateDF["end_date"]
				for loc in dateList:
					if(loc!=dateDestination):
						start_date = loc
						dateDF["start_date"] = start_date
			elif(end_date == ""):
				dateSource = dateDF["start_date"]
				for loc in dateList:
					if(loc!=dateSource):
						end_date = loc
						dateDF["end_date"] = end_date

		else:
			start_date = dateList[0]
			dateDF["start_date"] = start_date
			if(numDates == 2):
				end_date = dateList[1]
				dateDF["end_date"] = end_date
			
			
	#	print "Rule 4 applied"
		return dateDF



def checkInList(word,fileName):
	seedlist = []
	with open(fileName) as f:
		line = f.readline().strip()
		seedlist = line.split(",")
	if word in seedlist:
	    return 1
	return 0

def getDatePPChunks(dateList,parse):
	parse = re.sub(r'\(',"",parse)
	parse = re.sub(r'\)',"",parse)
	parse = parse.split(' ')

	print parse
	
	indexesPP = []
	indexesDate = []
	datePPChunks=[]

	for index, postag in enumerate(parse):
		if postag == 'PP' :
			indexesPP.append(index)
		if postag in dateList:
			indexesDate.append(index)

	resultIndexes = sorted(indexesPP + indexesDate)
	print resultIndexes

	for index, position in enumerate(resultIndexes):
		if position in indexesDate:
			datePPChunks.append(parse[resultIndexes[index-1]:(resultIndexes[index]+1)])
	return datePPChunks

def extractPrepositionFromChunk(chunk):
	for index, postag in enumerate(chunk):
		if postag == 'IN' or postag == 'TO':
			return chunk[index+1] 

def extractDateFromChunk(chunk):
	for index, postag in enumerate(chunk):
		if postag == 'NNP':
			return chunk[index+1] 

def checkPrepositionSource(preposition):
	return checkInList(preposition,DISAMBIGUATOR_DATE_SOURCE_PREPOSITIONS)

def checkPrepositionDestination(preposition):
	return checkInList(preposition,DISAMBIGUATOR_DATE_DESTINATION_PREPOSITIONS)
	
def getDateVPChunks(dateList,parse):
	parse = re.sub(r'\(',"",parse)
	parse = re.sub(r'\)',"",parse)
	parse = parse.split(' ')

	indexesVP = []
	indexesDate = []
	
	dateVPChunks=[]

	for index, postag in enumerate(parse):
		if postag == 'VP' :
			indexesVP.append(index)
		if postag in dateList:
			indexesDate.append(index)

	resultIndexes = sorted(indexesVP + indexesDate)

	for index, position in enumerate(resultIndexes):
		if position in indexesDate:
			dateVPChunks.append(parse[resultIndexes[index-1]:(resultIndexes[index]+1)])
	return dateVPChunks

def extractVerbFromChunk(chunk):
	for index, postag in enumerate(chunk):
		if(postag[:2] == "VB"):
			return chunk[index+1] 
	return ""

def extractRootForm(verbInflected,extendedNERAnalyzedParse):
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		if(tokenInfoDict["word"].lower() == verbInflected):
			return tokenInfoDict["lemma"].lower()
			
def checkVerbSource(verb):
	return checkInList(verb,DISAMBIGUATOR_DATE_SOURCE_VERB)

def checkVerbDestination(verb):
	return checkInList(verb,DISAMBIGUATOR_DATE_DESTINATION_VERB)	
	
def loadSeedlist(fileName):
	seedlist = []
	with open(fileName) as f:
		line = f.readline().strip()
		seedlist = line.split(",")
	return seedlist

def findPosition(seedlist,extendedNERAnalyzedParse):
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		for word in seedlist:
			if(tokenInfoDict["word"].lower() == word):
				return key
	return 0

def findSourcePosition(extendedNERAnalyzedParse,fileName):
	sourceList = loadSeedlist(fileName)
	return findPosition(sourceList,extendedNERAnalyzedParse)

def findDestinationPosition(extendedNERAnalyzedParse,fileName):
	destinationList = loadSeedlist(fileName)
	return findPosition(destinationList,extendedNERAnalyzedParse)
'''