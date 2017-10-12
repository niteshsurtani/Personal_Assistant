import pprint
import nltk
import math
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import unicodedata
import operator

pp = pprint.PrettyPrinter(indent=4)
stemmer = LancasterStemmer()

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

def getData():
	data = []
	questionDict = []
	f = open('data.txt','r')
	lines = f.readlines()

	for index in range(0,len(lines),3):
		dataDict = {}
		dataDict['question'] = lines[index].decode('utf-8').strip()
		dataDict['answer'] = lines[index + 1].decode('utf-8').strip()
		data.append(dataDict)
		questionDict.append(dataDict['question'])
	return questionDict, data

def createVocab(data):
	vocab = []

	for item in data:
		questionTokens = nltk.word_tokenize(item['question'])
		answerTokens = nltk.word_tokenize(item['answer'])
		
		for token in questionTokens:
			if token not in (stopwords.words('english')):
				vocab.append(stemmer.stem(token.lower()))
		
		for token in answerTokens:
			if token not in (stopwords.words('english')):
				vocab.append(stemmer.stem(token.lower()))

	return vocab

def createDictionary(vocab):
	d = {}
	for item in vocab:
		d[item] = 0
	return d

def createDataset(data, vocabDict):
	dataset = []
	count = 0

	for item in data:
		dataset.append(vocabDict.copy())
		di = dataset[count]
		questionTokens = nltk.word_tokenize(item['question'].lower())
		length_question = len(questionTokens)

		for token in questionTokens:
			if token in di:
				di[token] = di[token] + 10 * 1.0 / math.sqrt(length_question)
		
		answerTokens = nltk.word_tokenize(item['answer'].lower())
		length_answer = len(answerTokens)

		for token in answerTokens:
			if token in di:
				di[token] = di[token] + 1  * 1.0 / math.sqrt(length_answer)

		count += 1

	return dataset

def normalizeDataset(dataset, idfDict):
	for data in dataset:
		for key, item in idfDict.iteritems():
			if key in idfDict:
				idfDict[key] += data[key]

	for data in dataset:
		for key, item in idfDict.iteritems():
			if key in idfDict:
				if idfDict[key] == 0:
					data[key] = 0
				else:
					data[key] /= idfDict[key] * 1.0

	return dataset

def createTfIdf(data, vocab):
	vocabDict = createDictionary(vocab)
	dataset = createDataset(data, vocabDict)
	idfDict = createDictionary(vocab)
	dataset = normalizeDataset(dataset, idfDict)

	return dataset

def calculateMod(vector):
	mod = 0.0
	for key, value in vector.iteritems():
		mod += (value * value)

	root_mod = math.sqrt(mod)
	return root_mod

def cosineSimilarity(vocab, v1, v2):
	cosine_score = 0.0

	for value in vocab:
		cosine_score += v1[value] * v2[value]

	return cosine_score/(calculateMod(v1) * calculateMod(v2))

questionDict, data = getData()
vocab = createVocab(data)
tfidf = createTfIdf(data, vocab)


testData = [[{'question':'I want to cancel a ticket', 'answer': ''}], [{'question': 'I want to book a flight', 'answer': ''}], [{'question':'What documents should I carry', 'answer': ''}], [{'question':'Should I bring my credit card', 'answer': ''}]]

for item in testData:
	print item[0]['question']
	testIdf = createTfIdf(item, vocab)
	scores = {}

	index = 0
	for value in tfidf:
		scores[questionDict[index]] = cosineSimilarity(vocab, value, testIdf[0])
		index += 1

	sorted_score = sorted(scores.items(), key=operator.itemgetter(1))
	pp.pprint(sorted_score)
	print "\n"





