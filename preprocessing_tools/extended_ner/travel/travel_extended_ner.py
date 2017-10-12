import ner_classifier.classifier
import logging
from ner_classifier.PATH_CONSTANTS import *

def identifyExtendedNER(query,category,extendedNERAnalyzedParse,last_requested_DF,transport="all"):
	extended_ner_list = {}

	extractTransationItems(extendedNERAnalyzedParse)
	
	if(transport == "all"):
		transport = extractTransportItems(query,category,extended_ner_list,extendedNERAnalyzedParse)
	

	# =============== TRANSPORT GUESS MODULE WITH CLASS ================== #
	
	classTransport = extractClassItems(query,category,transport,extended_ner_list,extendedNERAnalyzedParse)

	if(transport != "all" and classTransport != "all" and transport != classTransport):
		print "##### TRANSPORT CONFLICT"
	elif(transport == "all"):
		transport = classTransport
	
	# ========================================================== #


	extractCity(extendedNERAnalyzedParse)
	extractOrganization(extendedNERAnalyzedParse)
	extractWeightItems(query,category,extended_ner_list,extendedNERAnalyzedParse)
	extractAmountItems(query,category,extended_ner_list,extendedNERAnalyzedParse)
	extractSeatPreferenceItems(query,category,transport,extended_ner_list,extendedNERAnalyzedParse)
	extractNumSeatsItems(query,category,extended_ner_list,extendedNERAnalyzedParse,last_requested_DF)
	extractNumStopsItems(query,category,extended_ner_list,extendedNERAnalyzedParse,last_requested_DF)
	extractTravelTypeItems(query,category,extended_ner_list,extendedNERAnalyzedParse,last_requested_DF)
	extractTimePreference(query,category,extended_ner_list,extendedNERAnalyzedParse,last_requested_DF)
	extractOtherPreference(query,category,extended_ner_list,extendedNERAnalyzedParse,last_requested_DF)
	extractNumResultsItems(query,category,extended_ner_list,extendedNERAnalyzedParse,last_requested_DF)
	
	normalizeTime(extendedNERAnalyzedParse)
	print "Before Range Handler"
	print extendedNERAnalyzedParse

	updateRangeInNER(extendedNERAnalyzedParse)

	print "After Range Handler"
	print extendedNERAnalyzedParse
	
	extendedNerDF = extractAllExtendedNER(extendedNERAnalyzedParse)
	# print "Ex = ",
	# print extendedNerDF
	return extendedNerDF

def extractTransationItems(extendedNERAnalyzedParse):
	# logging.info("Extracting transation items")
	ner_classifier.classifier.TransactionIdentifier(extendedNERAnalyzedParse)

def extractCity(extendedNERAnalyzedParse):
	# logging.info("Extracting cities")
	ner_classifier.classifier.extractCity(extendedNERAnalyzedParse)

def extractOrganization(extendedNERAnalyzedParse):
	# logging.info("Extracting Organiztions")
	ner_classifier.classifier.extractOrganization(extendedNERAnalyzedParse)

def extractTransportItems(query,category,ner_list,extendedNERAnalyzedParse):
	# logging.info("Extracting Transport Items")
	return ner_classifier.classifier.TransportIdentifier(query,category,ner_list,extendedNERAnalyzedParse)

def extractClassItems(query,category,transport,ner_list,extendedNERAnalyzedParse):
	# logging.info("Extracting class")
	return ner_classifier.classifier.ClassIdentifier(query,category,transport,ner_list,extendedNERAnalyzedParse)

def extractWeightItems(query,category,ner_list,extendedNERAnalyzedParse):
	# logging.info("Extracting weight terms")
	ner_classifier.classifier.WeightIdentifier(query,category,ner_list,extendedNERAnalyzedParse)

def extractAmountItems(query,category,ner_list,extendedNERAnalyzedParse):
	# logging.info("Extracting amount terms")
	ner_classifier.classifier.AmountIdentifier(query,category,ner_list,extendedNERAnalyzedParse)

def extractTrainQuotaItems(query,category,ner_list,extendedNERAnalyzedParse):
	# logging.info("Extracting train quota")
	ner_classifier.classifier.TrainQuotaIdentifier(query,category,ner_list,extendedNERAnalyzedParse)
	
def extractSeatPreferenceItems(query,category,transport,ner_list,extendedNERAnalyzedParse):
	# logging.info("Extracting seat preference")
	ner_classifier.classifier.SeatPreferenceIdentifier(query,category,transport,ner_list,extendedNERAnalyzedParse)

def extractNumSeatsItems(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF):
	# logging.info("Extracting number of seats")
	ner_classifier.classifier.NumSeatsIdentifier(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF)

def extractNumStopsItems(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF):
	# logging.info("Extracting number of stops")
	ner_classifier.classifier.NumStopsIdentifier(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF)

def extractNumResultsItems(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF):
	# logging.info("Extracting number of stops")
	ner_classifier.classifier.NumResultsIdentifier(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF)

def extractTravelTypeItems(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF):
	# logging.info("Extracting travel type")
	ner_classifier.classifier.TravelTypeIdentifier(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF)

def extractTimePreference(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF):
	# logging.info("Extracting travel type")
	ner_classifier.classifier.TimePreferenceIdentifier(extendedNERAnalyzedParse)

def extractOtherPreference(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF):
	# logging.info("Extracting travel type")
	ner_classifier.classifier.OtherPreferenceIdentifier(extendedNERAnalyzedParse)

def updateRangeInNER(extendedNERAnalyzedParse):
	ner_classifier.classifier.updateRangeInNER(extendedNERAnalyzedParse)
	

def normalizeTime(extendedNERAnalyzedParse):
	ner_classifier.classifier.timeNormalier(extendedNERAnalyzedParse)

def extractAllExtendedNER(extendedNERAnalyzedParse):
	extendedNerDF = {}
	ignoredDF = ['location','date','misc','number','ordinal']
	rangeDF = ['amount']

	#print extendedNERAnalyzedParse
	for key,tokenInfoDict in extendedNERAnalyzedParse.iteritems():
		nerKey = tokenInfoDict["NER"].lower()
		noNER = "O".lower()
		if(nerKey != noNER and nerKey not in ignoredDF):
			if "NormalizedNER" in tokenInfoDict:
				if(nerKey in rangeDF):
					if(nerKey in extendedNerDF):
						
						prevValue = extendedNerDF[nerKey]['exact']
						extendedNerDF[nerKey]['exact'] = ""
						if(float(tokenInfoDict["NormalizedNER"].strip()) > float(prevValue)):
							extendedNerDF[nerKey]['range']['max'] = tokenInfoDict["NormalizedNER"]
							extendedNerDF[nerKey]['range']['min'] = prevValue
						else:
							extendedNerDF[nerKey]['range']['max'] = prevValue
							extendedNerDF[nerKey]['range']['min'] = tokenInfoDict["NormalizedNER"]
					else:
						rangeType = {"range":{'min':"",'max':""},"exact":""}
						extendedNerDF[nerKey] = rangeType
						extendedNerDF[nerKey]['exact'] = tokenInfoDict["NormalizedNER"].rstrip()
				else:	
					extendedNerDF[nerKey] = tokenInfoDict["NormalizedNER"]
			else:
				if(tokenInfoDict["NER"].lower() == "organization"):
					nerKey = "company"
				extendedNerDF[nerKey] = tokenInfoDict["word"]
	return extendedNerDF