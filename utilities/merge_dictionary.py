# Merges the extendedNerDF to form a single DFList 
def mergeDictionaries(mainList,newList):
	k1 = mainList.keys()
	k2 = newList.keys()
	k = list(set(k1) | set(k2))

	for key in k:
		if key in k1 and key in k2 and type(mainList[key]) == list:
			for element in newList[key]:
				mainList[key].append(element)
		elif key in k1 and key in k2:
			mainList[key] = newList[key]
		else:
			if key in k2:
				if type(newList[key]) == list:
					mainList[key] = []
					for element in newList[key]:
						mainList[key].append(element)
				else:
					mainList[key] = newList[key]

	return mainList
