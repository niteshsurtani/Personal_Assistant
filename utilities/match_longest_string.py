def matchLongestString(extendedNERAnalyzedParse,key,item):
	matched_flag = 1
	item_list = item.split()
	ner_length = len(extendedNERAnalyzedParse)

	for index in range(0, len(item_list)):
		ner_index = key + index
		if ner_index > ner_length or extendedNERAnalyzedParse[ner_index]["word"].lower() != item_list[index].lower():
			matched_flag = 0
			break

	return matched_flag


def matchLongestStringQuery(tokens,key,item):

	matched_flag = 1
	item_list = item.split()
	item_length = len(item_list)
	
	query_length = len(tokens)

	for index in range(key, key + item_length):
		if index > query_length or tokens[index].lower() != item_list[index - key]:
			matched_flag = 0
			break

	return matched_flag

def annotateParse(extendedNERAnalyzedParse,key,item,annotation,marker):
	item_list = item.split()
	for index in range(0, len(item_list)):
		ner_index = key + index
		extendedNERAnalyzedParse[ner_index]['NER'] = marker
		extendedNERAnalyzedParse[ner_index]['NormalizedNER'] = annotation
