from xml.dom import minidom

def TruecaseDOMParse(directory,xmlFile):
	doc = minidom.parse(directory+"/"+xmlFile)
	query = []

	tokens = doc.getElementsByTagName("token")
	for token in tokens:
		wordTag = token.getElementsByTagName("TrueCaseText")[0]
		word = wordTag.firstChild.data
		query.append(word)
	return " ".join(query)

