import re
import sys
import codecs
import rules
import commons
	
def annotateNumbers(query, coreNLPData):
	'''
	(String,String) -> Object

	query
	=====
	I want to travel tomorrow morning
	
	corenlp_time
	============
	1 I PRP I 0 0
	2 want VBP want 0 0
	3 to TO to 0 0
	4 travel VB travel 0 0
	5 tomorrow NN tomorrow TIME 2015-09-30TMO
	6 morning NN morning TIME 2015-09-30TMO
	<parse>(ROOT (S (NP (PRP I)) (VP (VBP want) (S (VP (TO to) (VP (VB travel) (NP-TMP (NN tomorrow))))) (NP-TMP (NN morning)))))


	Takes the input query and CoreNLP Time annotated parse as string and annotates
	NUMBER tokens in that.

	INPUT: seventy two, 12, 14.1, 192.168.2.4
	OUTPUT: 72, 12, 14.1, no

	Cases to Handle
	1. 12
	2. 12.1
	3. seven hundred twenty four
	4. two fifty
	5. fifteen million
	6. single => 1
	7. 14,120
	8. 2 hundred four

	'''
	numbers = []
	
	## parses the coreNLPData to tokens and parse
	tokens, parse = commons.coreNLPDataParser(coreNLPData)

	index = 0
	count = 0
	flag = False
	strr=''
	str_out = {};
	
	## split the string into list
	words = query.lower().split()
	
	## loop thru words
	for word in words:
		## remove white spaces
		word = word.strip().replace(',','')
		## check if the word has any characters and tokens list has specified index 
		if len(word) != 0 and index < len(tokens):
			attributes = tokens[index].split()
			numbers.append(attributes)
			## checks for integer and float
			if (re.match(r'\d+(\.\d+)?', word) and attributes[4] == "0"):
				## if "." is presented in word look it as integer else its a integer
				if "." not in word:
					## check the lenght > 0 to escape out of bound error
					if len(re.findall(r'\d+', word)) > 0:
						attributes[4] = "NUMBER"
						attributes[5] = re.findall(r'\d+', word)[0]
				else:
					## check the lenght > 0 to escape out of bound error
					if len(re.findall(r'\d+', word)) > 0:
						attributes[4] = "NUMBER"
						attributes[5] = re.findall(r'\d+', word)[0] + re.findall(r'\d+(\.\d+)?', word)[0]
			elif word in rules.allnum:
				if(attributes[4] == "0"):
					attributes[4] = "NUMBER"
					# attributes[5] = word
					flag = True
					strr = strr+' '+word
				#print strr
			else:
				if word=='and' and flag:
					if(attributes[4]=="0"):
						attributes[4] = "NUMBER"

						# attributes[5] = word
						flag = True
						strr = strr+' '+word
				else:
					if flag and (word is not 'and') and (word not in rules.allnum):
						flag=False
						str_out = strr
						strr=''
		# At this point we have all the strings with numbers so we will proceed here to extract digits
						if (str_out.strip() in rules.dict1) and attributes[4]=="0":
							# attributes[4] = "NUMBER"
							numbers[len(numbers)-2][5] = rules.dict1[str_out.strip()]
						else:
							wordss = str_out.strip().split()
							sum1 = 0
							sum_out = 0
							str2 = ''
							fg = False
							gf_count = 0
							for t in wordss:
								if t in rules.dict1:
									sum1 = sum1 + rules.dict1[t]
								elif t in rules.dict2:
									if sum1 is not 0:
										sum_out = sum_out+ sum1*rules.dict2[t]
										sum1 = 0
									else:
										sum_out = rules.dict2[t]
							sum_out = sum_out + sum1
							if(attributes[4]=="0"):
								numbers[len(numbers)-2][5] = sum_out
								# attributes[4] = "NUMBER"
								# attributes[5] = sum_out
		index += 1

	flag = 0
	num = ""
	for number in reversed(numbers):
		if number[4] == "NUMBER" and number[5] != "0":
			num = number[5]
			flag = 1
		elif flag == 1 and number[4] == "NUMBER" and number[5] == "0":
			number[5] = num
		else:
			flag = 0

	finalOutput = ""
	flag = 0
	sentence = 0
	for number in numbers:
		if number[0] == "1":
			if flag == 1:
				finalOutput += parse[sentence] +"\n"
				sentence += 1
			flag = 1

		for index in number:
			# if index <= len(number)-2:
			# 	print number[index]+",",
			# else:
			finalOutput += str(index) + " "
		finalOutput += "\n"
	finalOutput += parse[sentence] +"\n"
	return finalOutput
	
# query_data = "1,30 want to travel tomorrow morning    "
# core_nlp_data = "1 1,30 PRP 1,30 0 0\n2 want VBP want 0 0\n3 to TO to 0 0\n4 travel VB travel 0 0\n5 yesterday NN yesterday TIME 2015-09-30TMO\n6 morning NN morning TIME 2015-09-30TMO\n<parse>(ROOT (S (NP (PRP I)) (VP (VBP want) (S (VP (TO to) (VP (VB travel) (NP-TMP (NN tomorrow))))) (NP-TMP (NN morning)))))"
# print "output \n", annotateNumbers(query_data, core_nlp_data)