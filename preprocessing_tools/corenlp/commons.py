import re
def coreNLPDataParser(corenlp_time):
	tokens = []
	parse = []

	lines = corenlp_time.split("\n")
	for line in lines:
		if "<parse>" in line:
			parse.append(line.strip())
		else:
			tokens.append(line.rstrip())
	return tokens, parse
	
def removeSpecialCharacters(query):
	return ''.join(e for e in query if e.isalnum())
	
def removeASpecialCharacter(query, character):
	return re.sub(character, '', query)
	
