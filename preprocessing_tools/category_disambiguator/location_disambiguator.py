import os
import nltk
import re
from PATH_CONSTANTS import *
	
def getNumberOfLocation(extendedNERAnalyzedParse):
	locationList = []
	locationCode = {}
	fl = 0
	locStr = ""
	normStr = ""
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		if(tokenInfoDict["NER"] == "LOCATION" and fl == 0):
			fl = 1
			locStr += tokenInfoDict["word"] + " "
			normStr = tokenInfoDict["NormalizedNER"]
		elif(tokenInfoDict["NER"] == "LOCATION" and fl == 1):
			if(normStr == tokenInfoDict["NormalizedNER"]):
				# print "Word = "+tokenInfoDict["word"]
				locStr += tokenInfoDict["word"] + " "
			else:
				locationList.append(locStr.strip())
				locStr = ""
				locStr += tokenInfoDict["word"] + " "
				normStr = tokenInfoDict["NormalizedNER"]
		else:
			if fl == 1:
				locationList.append(locStr.strip())
				locationCode[locStr.strip()] = normStr

				locStr = ""
			fl = 0
	if fl == 1:
		locationList.append(locStr.strip())
		locationCode[locStr.strip()] = normStr

	return locationList, locationCode

def disambiguateLocations(locationList,locationCode,extendedNERAnalyzedParse,chunkedParse,numLocations):
	# Step 1: Use the chunk information to find if prepositions are giving us the information
	locationDF = {}

	source = ""
	destination = ""
	
	prepositionChunkList = getLocationPPChunks(locationList,chunkedParse)

	for chunk in prepositionChunkList:
		prep = extractPrepositionFromChunk(chunk)
		location = extractLocationFromChunk(chunk)

		if(checkPrepositionSource(prep)):
			source = location
			locationDF["source"] = source
		elif(checkPrepositionDestination(prep)):
			destination = location
			locationDF["destination"] = destination

	if(len(locationDF) == numLocations):
#		print "Rule 1 applied"
		for key,loc in locationDF.iteritems():
			locationDF[key] = locationCode[loc]
		return locationDF


	# Step 2. If no information from step 1, then use verbs 
	verbInflected = ""
	verbChunkList = getLocationVPChunks(locationList,chunkedParse)
#	print "Chunk List"
#	print verbChunkList
	for chunk in verbChunkList:
		verbInflected = extractVerbFromChunk(chunk)
		if(verbInflected != ""):
			verbInflected = verbInflected.lower()
		verb = extractRootForm(verbInflected,extendedNERAnalyzedParse)
#		print "Root verb form = " + verb
		location = extractLocationFromChunk(chunk)
#		print "Location = "+location
		if(checkVerbSource(verb)):
			source = location
			locationDF["source"] = source
		elif(checkVerbDestination(verb)):
			destination = location
			locationDF["destination"] = destination
			
	if(len(locationDF) == numLocations):
#		print "Rule 2 applied"
		for key,loc in locationDF.iteritems():
			locationDF[key] = locationCode[loc]

		return locationDF


	# Step 3. If no verb matched, find SOURCE and DESTINATION keywords in the query.
	sourcePosition = 0
	destinationPosition = 0

	sourcePosition = findSourcePosition(extendedNERAnalyzedParse,DISAMBIGUATOR_LOCATION_SOURCE_KEYWORDS)
	destinationPosition = findDestinationPosition(extendedNERAnalyzedParse,DISAMBIGUATOR_LOCATION_DESTINATION_KEYWORDS)

	if(sourcePosition !=0  and destinationPosition != 0):
		if(sourcePosition < destinationPosition):
			source = locationList[0]
			destination = locationList[1]
			locationDF["source"] = source
			locationDF["destination"] = destination
		else:
			source = locationList[1]
			destination = locationList[0]
			locationDF["source"] = source
			locationDF["destination"] = destination

	elif(sourcePosition != 0  and destinationPosition == 0):
		# Pick location from locationList not in locationDF['destination']
		if(numLocations == 1):
			locationDF["source"] = locationList[0]
		elif(numLocations == 2):
			if("destination" in locationDF.keys()):
				locationDestination = locationDF["destination"]
				for loc in locationList:
					if(loc!=locationDestination):
						source = loc
						locationDF["source"] = source
			else:
				locationDF["source"] = locationList[0]

	elif(sourcePosition ==0  and destinationPosition != 0):
		if(numLocations == 1):
			locationDF["destination"] = locationList[0]
		elif(numLocations == 2):
			if("source" in locationDF.keys()):
				locationSource = locationDF["source"]
				for loc in locationList:
					if(loc!=locationSource):
						destination = loc
						locationDF["destination"] = destination
			else:
				locationDF["destination"] = locationList[0]

	if(len(locationDF) == numLocations):
#		print "Rule 3 applied"
		for key,loc in locationDF.iteritems():
			locationDF[key] = locationCode[loc]

		return locationDF
	
	print "DF = ",
	print locationDF
	# Step 4. Treat first location as Source and second location as Destination.
	if(len(locationDF) == 1):
		if not "source" in locationDF.keys():
			locationDestination = locationDF["destination"]
			for loc in locationList:
				if(loc!=locationDestination):
					source = loc
					locationDF["source"] = source
		if not "destination" in locationDF.keys():
			locationSource = locationDF["source"]
			for loc in locationList:
				if(loc!=locationSource):
					destination = loc
					locationDF["destination"] = destination

	else:
		if(len(locationList) == 2):
			source = locationList[0]
			locationDF["source"] = source
			if(numLocations == 2):
				destination = locationList[1]
				locationDF["destination"] = destination
		# else:
		# 	locationDF["source"] = locationList[0]
		
#	print "Rule 4 applied"
	for key,loc in locationDF.iteritems():
		locationDF[key] = locationCode[loc]

	return locationDF




def checkInList(word,fileName):
	seedlist = []
	with open(fileName) as f:
		line = f.readline().strip()
		seedlist = line.split(",")
	if word in seedlist:
	    return 1
	return 0

def getLocationPPChunks(locationList,parse):
	parse = re.sub(r'\(',"",parse)
	parse = re.sub(r'\)',"",parse)
	parse = parse.split(' ')

	indexesPP = []
	indexesLocation = []
	locationPPChunks=[]

	print locationList

	for index, postag in enumerate(parse):
		print index, postag
		if postag == 'PP':
			indexesPP.append(index)
		if postag in locationList:
			indexesLocation.append(index)

	resultIndexes = sorted(indexesPP + indexesLocation)
	print resultIndexes

	for index, position in enumerate(resultIndexes):
		if position in indexesLocation:
			locationPPChunks.append(parse[resultIndexes[index-1]:(resultIndexes[index]+1)])
	return locationPPChunks

def extractPrepositionFromChunk(chunk):
	for index, postag in enumerate(chunk):
		if postag == 'IN' or postag == 'TO':
			return chunk[index+1] 

def extractLocationFromChunk(chunk):
	for index, postag in enumerate(chunk):
		if postag in ('NN','NNP'):
			return chunk[index+1] 

def checkPrepositionSource(preposition):
	return checkInList(preposition,DISAMBIGUATOR_LOCATION_SOURCE_PREPOSITIONS)

def checkPrepositionDestination(preposition):
	return checkInList(preposition,DISAMBIGUATOR_LOCATION_DESTINATION_PREPOSITIONS)

def getLocationVPChunks(locationList,parse):
	parse = re.sub(r'\(',"",parse)
	parse = re.sub(r'\)',"",parse)
	parse = parse.split(' ')

	indexesVP = []
	indexesLocation = []
	
	locationVPChunks=[]

	for index, postag in enumerate(parse):
		if postag == 'VP' :
			indexesVP.append(index)
		if postag in locationList:
			indexesLocation.append(index)

	resultIndexes = sorted(indexesVP + indexesLocation)

	for index, position in enumerate(resultIndexes):
		if position in indexesLocation:
			locationVPChunks.append(parse[resultIndexes[index-1]:(resultIndexes[index]+1)])
	return locationVPChunks

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
	return checkInList(verb,DISAMBIGUATOR_LOCATION_SOURCE_VERB)

def checkVerbDestination(verb):
	return checkInList(verb,DISAMBIGUATOR_LOCATION_DESTINATION_VERB)	
	
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
