# -*- coding: utf-8 -*-
import rules
import math
import re

def solveNumber(query):
	# print query
	
	query = splitCamma(query)
	query = improveQuery(query)
	
	## list to find all possible number locations
	possibleLocation = []
	## tracks queryIndex
	queryIndex = 0;
	processedQuery = query.replace('hundred and', 'hundred').replace(' ', '_')
	
	rawData = query.replace('hundred and', 'hundred').split()
	
	for value in rawData:
		value = value.replace(',', '')
		if value in rules.allnum:
			possibleLocation.append(queryIndex)	
		queryIndex += 1;
	
	previousPosition = -1;
	numbers = []
	positionListIndex = 0;
	
	for currentPosition in possibleLocation:
		if(previousPosition != -1):
			if(previousPosition + 1 == currentPosition):
				numbers.append(rawData[currentPosition])
				if(positionListIndex == len(possibleLocation)-1):
					processedQuery = processedQuery.replace('_'.join(numbers), solveTheNumberToString(numbers))
			else:
				processedQuery = processedQuery.replace('_'.join(numbers), solveTheNumberToString(numbers))
				previousPosition = -1;
				del numbers[:]
				numbers.append(rawData[currentPosition])
				if(positionListIndex == len(possibleLocation)-1):
					processedQuery = processedQuery.replace('_'.join(numbers), solveTheNumberToString(numbers))
		else:
			numbers.append(rawData[currentPosition])
			if(positionListIndex == len(possibleLocation)-1):
				processedQuery = processedQuery.replace('_'.join(numbers), solveTheNumberToString(numbers))
				
		positionListIndex += 1
		previousPosition = currentPosition
	
	return processedQuery.replace('_', ' ')
	
def solveTheNumberToString(numbersWordList):
	solvedNumber = 0;
	numbersList = convertWordsToNumber(numbersWordList)
	sortedList = sorted(numbersList, key=int, reverse=True)
	if sortedList == numbersList:
		reversesortedList = sorted(numbersList)
		previousValue = -1
		fail = None
		if(len(reversesortedList) > 1):
			for number in reversesortedList:
				if(previousValue == -1):
					previousValue = number
				else:
					if(len(str(previousValue)) >= len(str(number))):
						fail = True;
						
		if(not fail):
			for number in sortedList:
				solvedNumber += number
		else:
			for number in sortedList: 
				solvedNumber += int(str(number))
	else:
		curedNumbersList = cureList(numbersList)
		solvedNumber = convertUnits(curedNumbersList)	
				
	if solvedNumber == 0:
		return ' '.join(numbersWordList)
	else:		
		return str(solvedNumber)
		
def convertUnits(numbersList):
	while True:
		number1 = 0
		number2 = 0
		if(len(numbersList) != 1):
			number1 = numbersList.pop(-1)
		else:
			return numbersList[0]
		if(len(numbersList) == 0):
			return 0
		if(len(numbersList) > 0):
			number2 = numbersList.pop(-1)
			fail = None
			if(len(str(number1)) > len(str(number2))):
				fail = True;				
			if(not fail):
				number2 += number1
			else:
				if(int(str(number1)[:1]) == 1):
					number2 = int(str(number2) + str(number1)[1:])
				else:
					number3 = number2 + int(str(number1)[:1])
					number2 = int(str(number3) + str(number1)[1:])
			numbersList.append(number2)
	return 0
	
def cureList(numbersList):
	curedList = []
	while True:
		number1 = 0
		number2 = 0
		takeNumber = None;
		if(len(numbersList) == 0):
			return curedList
		if(len(numbersList) != 1):
			if(len(curedList) > 0):
				number1 = curedList[-1]
				takeNumber = False;
			else:
				number1 = numbersList.pop(0)
				takeNumber = True;
		else:
			curedList.append(numbersList.pop(0))
			return curedList
		if(len(numbersList) > 0):
			number2 = numbersList.pop(0)
			if(number1 in rules.allUnits or number2 in rules.allUnits):
				if(takeNumber):
					curedList.append(number1)
				curedList.append(number2)
			else:
				if(takeNumber):
					curedList.append(number1)
				curedList.append(getRoundedUnit(len(str(number2))))
				curedList.append(number2)
				
	return curedList

def splitCamma(query):
	splitedCammaQuery = []
	for word in query.split():
		if(word[-1:] == ',' and word[1:] == ','):
			splitedCammaQuery.append(word.replace(',',' , '))
		elif(word[-1:] == ','):
			splitedCammaQuery.append(word.replace(',',' ,'))
		elif(word[1:] == ','):
			splitedCammaQuery.append(word.replace(',',', '))
		else:
			splitedCammaQuery.append(word)
			
	return ' '.join(splitedCammaQuery)
	
def improveQuery(query):
	letters = set(',')
	improvedQuery = []
	for word in query.split():
		if letters & set(word):
			if(len(word.strip()) > 1):
				cammaList = word.split(',')
				currentState = 3;
				dummyCammaList = cammaList
				valid = None
				canChange = None
				for position in cammaList:
					# print cammaList[-1]
					currentUnit = dummyCammaList.pop(-1)
					if(len(currentUnit.strip()) > 0):
						if(len(str(currentUnit)) == 3 or len(str(currentUnit)) == 2):
							if(len(str(currentUnit)) == 2 and canChange == None):
								canChange = False	
								currentState = len(str(currentUnit))
								
							if(len(str(currentUnit)) == currentState):
								currentState = len(str(currentUnit))
							else:
								valid = False
						elif(len(str(currentUnit)) == 1 or len(str(currentUnit)) == 0 or len(str(currentUnit)) > 3):
							valid = False
					else:
						valid = False
						
				if(valid == None):
					word = word.replace(',','')
				improvedQuery.append(word)
		else:
			improvedQuery.append(word)
	return ' '.join(improvedQuery)
	
def addToList(list, number, index):
	return list[:index] + [number] + a[index:]
	
def getRoundedUnit(size):
	return int(math.pow(10, size))
	
def getListOfDuplicates(numbersList, number):
	return [i for i,x in enumerate(numbersList) if x == number]
	
def convertWordsToNumber(numbersList):
	convertedList = []
	for number in numbersList:
		convertedList.append(rules.dict3[number])
	return convertedList
	
def int_to_en(num):
    d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'ninteen', 20 : 'twenty',
          30 : 'thirty', 40 : 'fourth', 50 : 'fifty', 60 : 'sixty',
          70 : 'seventy', 80 : 'eighty', 90 : 'ninty' }
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    assert(0 <= num)

    if (num < 20):
        return d[num]

    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] + ' ' + d[num % 10]

    if (num < k):
        if num % 100 == 0: return d[num // 100] + ' hundred'
        else: return d[num // 100] + ' hundred and ' + int_to_en(num % 100)

    if (num < m):
        if num % k == 0: return int_to_en(num // k) + ' thousand'
        else: return int_to_en(num // k) + ' thousand, ' + int_to_en(num % k)

    if (num < b):
        if (num % m) == 0: return int_to_en(num // m) + ' million'
        else: return int_to_en(num // m) + ' million, ' + int_to_en(num % m)

    if (num < t):
        if (num % b) == 0: return int_to_en(num // b) + ' billion'
        else: return int_to_en(num // b) + ' billion, ' + int_to_en(num % b)

    if (num % t == 0): return int_to_en(num // t) + ' trillion'
    else: return int_to_en(num // t) + ' trillion, ' + int_to_en(num % t)

    raise AssertionError('num is too large: %s' % str(num))
	
