import os
import sys,ast
#from genie_nlp import nlp_preprocessing_engine
from preprocessing_tools.abbreviation_checker.number_string_splitter import number_string_splitter
import os
import nltk
import collections

# Loads all the static variables to be used globally.
from FILE_CONSTANTS import *
import logging

import preprocessing_tools.spell_checker.spell_checker
import preprocessing_tools.truecase.truecase
import preprocessing_tools.corenlp.corenlp
import preprocessing_tools.category_disambiguator.category_disambiguator
import preprocessing_tools.extended_ner.food.food_extended_ner
import preprocessing_tools.extended_ner.travel.travel_extended_ner
import preprocessing_tools.abbreviation_checker.abbr_corrector

import filecmp
#number_string_splitter("hello hi","preprocessing_tools/abbreviation_checker/rules")
query_file="testing/testcases/queries"
splitter_gold="testing/testcases/queries_splitted_gold"
splitter_out="testing/testcases/queries_splitted_out"
abbr_gold_f="testing/testcases/queries_abbr_gold"
abbr_out_f="testing/testcases/queries_abbr_out"
spell_gold_f="testing/testcases/queries_spell_gold"
spell_out_f="testing/testcases/queries_spell_out"
ner_parse_out_f="testing/testcases/queries_ner_parse_out"
ner_parse_gold_f="testing/testcases/queries_ner_parse_gold"
exner_out_f="testing/testcases/queries_exner_out"
exner_gold_f="testing/testcases/queries_exner_gold"
rules_directory="preprocessing_tools/abbreviation_checker/rules"

#To create gold data for testing splitter ( first system output is taken and then manually post-processed to get gold data)
def createGoldSplitter():
	w=open(splitter_gold,"w")
	for query in open(query_file,"r"):
		query = query.lower()
		splitted=number_string_splitter(query,rules_directory).strip()
		w.write(str(splitted)+"\n")
	w.close()
	#edit the file manually to correct the errors


#to test the splitter module given query file and gold output
def testSplitter():
	correct_count=0
	total_count=0
	w=open(splitter_out,"w")
	f=open(splitter_gold,"r")
	for query in open(query_file,"r"):
		query=query.lower()
		total_count+=1
		splitted_out=number_string_splitter(query,rules_directory).strip()
		w.write(str(splitted_out)+"\n")
		splitted_gold=f.readline().strip()
		if splitted_out==splitted_gold:
			correct_count+=1
	w.close()
	f.close()
	return correct_count, total_count




#=====================================================================================================
#To create gold data for testing abbr corrector ( first system output is taken and then manually post-processed to get gold data)
def createGoldAbbr():
	w=open(abbr_gold_f,"w")
	for query in open(splitter_gold,"r"):
		abbr=preprocessing_tools.abbreviation_checker.abbr_corrector.abbr_detector(query,RULES_DIRECTORY,FILENAME).strip()
		w.write(str(abbr)+"\n")
	w.close()
	#edit file manually to correct the errors

#to test the abbr corrector module given query file and gold output
def testAbbr():
	correct_count=0
	total_count=0
	w=open(abbr_out_f,"w")
	f=open(abbr_gold_f,"r")
	for query in open(splitter_gold,"r"):
		total_count+=1
		abbr_out=preprocessing_tools.abbreviation_checker.abbr_corrector.abbr_detector(query,RULES_DIRECTORY,FILENAME).strip()
		w.write(str(abbr_out)+"\n")
		#print abbr_out
		abbr_gold=f.readline().strip()
		if abbr_out==abbr_gold:
			correct_count+=1
	w.close()
	f.close()
	return correct_count, total_count


#================================================================================================


#To create gold data for testing spell corrector ( first system output is taken and then manually post-processed to get gold data)
def createGoldSpell():
	w=open(spell_gold_f,"w")
	for query in open(abbr_gold_f,"r"):
		spell=preprocessing_tools.spell_checker.spell_checker.spellCheck(query,PWL_FILE,OTHER_WORDS_FILE).strip()
		w.write(str(spell)+"\n")
	w.close()
	#edit file manually to correct the errors

#to test the spell corrector module given query file and gold output
def testspell():
	correct_count=0
	total_count=0
	w=open(spell_out_f,"w")
	f=open(spell_gold_f,"r")
	for query in open(abbr_gold_f,"r"):
		total_count+=1
		spell_out=preprocessing_tools.spell_checker.spell_checker.spellCheck(query,PWL_FILE,OTHER_WORDS_FILE).strip()
		w.write(str(spell_out)+"\n")
		spell_gold=f.readline().strip()
		if spell_out==spell_gold:
			correct_count+=1
	w.close()
	f.close()
	return correct_count, total_count


#===============================================================================================



#To create gold data for testing spell corrector ( first system output is taken and then manually post-processed to get gold data)
def createGoldSpell():
	w=open(spell_gold_f,"w")
	for query in open(abbr_gold_f,"r"):
		spell=preprocessing_tools.spell_checker.spell_checker.spellCheck(query,PWL_FILE,OTHER_WORDS_FILE).strip()
		w.write(str(spell)+"\n")
	w.close()
	#edit file manually to correct the errors

#to test the spell corrector module given query file and gold output
def testspell():
	correct_count=0
	total_count=0
	w=open(spell_out_f,"w")
	f=open(spell_gold_f,"r")
	for query in open(abbr_gold_f,"r"):
		total_count+=1
		spell_out=preprocessing_tools.spell_checker.spell_checker.spellCheck(query,PWL_FILE,OTHER_WORDS_FILE).strip()
		w.write(str(spell_out)+"\n")
		spell_gold=f.readline().strip()
		if spell_out==spell_gold:
			correct_count+=1
	w.close()
	f.close()
	return correct_count, total_count


#===============================================================================================


#To create gold data for testing NERParse and chunkParse ( first system output is taken and then manually post-processed to get gold data)
def createGoldNerParse():
	w=open(ner_parse_gold_f,"w")
	for query in open(spell_gold_f,"r"):
		NERAnalyzedParse, chunkedParse = preprocessing_tools.corenlp.corenlp.identifyNER(CORENLP_INPUT,CORENLP_GENERATED_FILE,PWD,CORENLP_DIRECTORY,CORENLP_TOOL_DIRECTORY,CONFIG_CORENLP,query)
		w.write(str(NERAnalyzedParse)+"\n")
		w.write(str(chunkedParse)+"\n")
	w.close()
	#edit file manually to correct the errors

#to test the NERParse and chunkParse modules given query file and gold output
def testNerParse():
	correct_ner_count=0
	correct_parse_count=0
	total_count=0
	w=open(ner_parse_out_f,"w")
	f=open(ner_parse_gold_f,"r")
	for query in open(spell_gold_f,"r"):
		total_count+=1
		NERAnalyzedParse_out, chunkedParse_out = preprocessing_tools.corenlp.corenlp.identifyNER(CORENLP_INPUT,CORENLP_GENERATED_FILE,PWD,CORENLP_DIRECTORY,CORENLP_TOOL_DIRECTORY,CONFIG_CORENLP,query)
		w.write(str(NERAnalyzedParse_out)+"\n")
		w.write(str(chunkedParse_out)+"\n")
		NERAnalyzedParse_gold = ast.literal_eval(f.readline().strip())
		chunkedParse_gold = ast.literal_eval(f.readline().strip())
		if NERAnalyzedParse_out==NERAnalyzedParse_gold:
			correct_ner_count+=1
		if chunkedParse_gold==chunkedParse_out:
			correct_parse_count+=1
	w.close()
	f.close()
	return correct_ner_count, correct_parse_count, total_count


#=================================================================================================


#To create gold data for extendedNER ( first system output is taken and then manually post-processed to get gold data)
def createGoldExNerParse():
	w=open(exner_gold_f,"w")
	f=open(ner_parse_gold_f,"r").readlines()
	x=0
	spell_file=open(spell_gold_f,"r").readlines()
	while x<len(f)-1:
		allExtendedNerDF={}
		if f[x]=="" or f[x]=="\n":
			x+=1
			continue
		NERAnalyzedParse=ast.literal_eval(f[x].strip())
		chunkedParse=ast.literal_eval(f[x+1].strip())
		for index in range(0,len(chunkedParse)):
			entitiesList = preprocessing_tools.extended_ner.food.food_extended_ner.identifyExtendedNER(spell_file[x/2],NERAnalyzedParse[index],chunkedParse[index])
			singleExtendedNerDF = preprocessing_tools.extended_ner.food.food_extended_ner.disambiguateTokens(NERAnalyzedParse[index],entitiesList)
			allExtendedNerDF = mergeDictionaries(allExtendedNerDF,singleExtendedNerDF)
		w.write(str(allExtendedNerDF)+"\n")
		x+=2
	w.close()
	#edit file manually to correct the errors

#to test the extendedNER module given query file and gold output
def testExNerParse():
	correct_count=0
	total_count=0
	w=open(exner_out_f,"w")
	fex=open(exner_gold_f,"r")
	f=open(ner_parse_gold_f,"r").readlines()
	x=0
	spell_file=open(spell_gold_f,"r").readlines()
	while x <len(f):
		total_count+=1
		allExtendedNerDF={}
		if f[x]=="" or f[x]=="\n":
			x+=1
		NERAnalyzedParse=ast.literal_eval(f[x].strip())
		chunkedParse=ast.literal_eval(f[x+1].strip())
		for index in range(0,len(chunkedParse)):
			entitiesList = preprocessing_tools.extended_ner.food.food_extended_ner.identifyExtendedNER(spell_file[x/2],NERAnalyzedParse[index],chunkedParse[index])
			singleExtendedNerDF = preprocessing_tools.extended_ner.food.food_extended_ner.disambiguateTokens(NERAnalyzedParse[index],entitiesList)
			allExtendedNerDF = mergeDictionaries(allExtendedNerDF,singleExtendedNerDF)
		w.write(str(allExtendedNerDF)+"\n")
		x+=2
		if allExtendedNerDF==ast.literal_eval(fex.readline().strip()):
			correct_count+=1
		return correct_count,total_count


		NERAnalyzedParse_out, chunkedParse_out = preprocessing_tools.corenlp.corenlp.identifyNER(CORENLP_INPUT,CORENLP_GENERATED_FILE,PWD,CORENLP_DIRECTORY,CORENLP_TOOL_DIRECTORY,CONFIG_CORENLP,query)
		w.write(str(NERAnalyzedParse_out)+"\n")
		w.write(str(chunkedParse_out)+"\n")
		NERAnalyzedParse_gold = ast.literal_eval(f.readline().strip())
		chunkedParse_gold = ast.literal_eval(f.readline().strip())
		if NERAnalyzedParse_out==NERAnalyzedParse_gold:
			correct_ner_count+=1
		if chunkedParse_gold==chunkedParse_out:
			correct_parse_count+=1
	w.close()
	f.close()
	return correct_ner_count, correct_parse_count, total_count



#====================================================================================================

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









createGoldSplitter()
print testSplitter()
createGoldAbbr()
"""print testAbbr()
createGoldSpell()
print testspell()
createGoldNerParse()
print testNerParse()
createGoldExNerParse()
print testExNerParse()"""