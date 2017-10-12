from xml.dom import minidom

# xmlFile is the path of the XMLFile.
def Main(xmlFile,request):
	doc = minidom.parse(xmlFile)

	# doc.getElementsByTagName returns NodeList

	tokens = doc.getElementsByTagName("token")
	if(request == "AllLocations"):
		return getAllLocations(tokens)
	elif(request == "AllDates"):
		return getAllDates(tokens)
	

def convertXMLToDict(xmlFile):
    	print xmlFile
	doc = minidom.parse(xmlFile)
	chunkedParse = doc.getElementsByTagName("parse")[0].firstChild.nodeValue
	tokens = doc.getElementsByTagName("token")
	index = 1
	tokensInformation = {}
	for token in tokens:
		tokenParameters = {}
		tokensInformation[index] = tokenParameters
		for node in token.childNodes:
			if node.nodeType == node.ELEMENT_NODE:
				# Not a timex node, since it doesn't holds any data
				if(node.tagName != "Timex"):
					tokenParameters[node.tagName] = token.getElementsByTagName(node.tagName)[0].firstChild.data
		index = index + 1
		
	return tokensInformation,chunkedParse

def getAllLocations(tokens):
	locations = {}
	locationList = []
	tokenList = []
	locationFlag = 0
	for token in tokens:
		nerTag = token.getElementsByTagName("NER")[0]
		ner = nerTag.firstChild.data
		if(ner=="LOCATION"):
			wordTag = token.getElementsByTagName("word")[0]
			word = wordTag.firstChild.data
			token_id = token.getAttribute("id")
			locationList.append(word)
			tokenList.append(token_id)
			locationFlag = 1
		else:
			if(locationFlag == 1):
				completeLocation = " ".join(locationList)
				completeToken = "_".join(tokenList)
				locations[completeToken]=completeLocation
				locationFlag = 0
				locationList = []
				tokenList = []
	return locations
	
def getAllDates(tokens):
	dates = {}
	finalDate = ""
	finalToken = 0
	dateFlag = 0
	for token in tokens:
		nerTag = token.getElementsByTagName("NER")[0]
		ner = nerTag.firstChild.data
		if(ner=="DATE"):
			NormalizedNERTag = token.getElementsByTagName("NormalizedNER")[0]
			NormalizedNER = NormalizedNERTag.firstChild.data
			token_id = token.getAttribute("id")
			dateFlag = 1
			finalDate = NormalizedNER
			finalToken = token_id
		else:
			if (dateFlag == 1):
			 	dates[finalToken] = finalDate
				dateFlag = 0
	return dates
