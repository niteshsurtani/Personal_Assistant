################## CLASS IDENTIFICATION ######################
import ner_class
import ner_weight
import ner_amount
import ner_train_quota
import ner_seat_preference
import ner_num_seats
import ner_num_stops
import ner_num_results
import ner_travel_type
import ner_transport
import ner_transaction
import ner_city
import ner_organization
import ner_time_preference
import ner_other_preference
import time_normalizer
import range_handler

import nltk
import os

from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *
from PATH_CONSTANTS import *

# A wrapper function to mark all the identified categories in the xml file.
def TransportIdentifier(query,category,ner_list,extendedNERAnalyzedParse):
	return ner_transport.getTransport(extendedNERAnalyzedParse)

def TransactionIdentifier(extendedNERAnalyzedParse):
	ner_transaction.getTransaction(extendedNERAnalyzedParse)


def extractCity(extendedNERAnalyzedParse):
	ner_city.findCity(extendedNERAnalyzedParse)

def TimePreferenceIdentifier(extendedNERAnalyzedParse):
	ner_time_preference.getTimePreference(extendedNERAnalyzedParse)

def OtherPreferenceIdentifier(extendedNERAnalyzedParse):
	ner_other_preference.getOtherPreference(extendedNERAnalyzedParse)

def extractOrganization(extendedNERAnalyzedParse):
	ner_organization.findOrganization(extendedNERAnalyzedParse)
#
def ClassIdentifier(query,category,transport,ner_list,extendedNERAnalyzedParse):
	transport = "flight"
	if(ner_class.existClass(query)):
#		print "Class exists"
		seed = ner_class.loadClassSeedlist(transport)

		bypassTransportFlag = 0
		if(transport == "all"):
			bypassTransportFlag = 1

		# Transport and Class identified by extended NER
		finalTransport = ""
		finalClass = ""

		classMatchedFlag = 0
		for key in seed:
			if(transport == key or bypassTransportFlag == 1):
				for classType in seed[key]:
					classTypePatterns = ner_class.loadClassTypePatterns(key,classType)
					if(ner_class.matchedClass(query,classType,classTypePatterns,extendedNERAnalyzedParse)):
						finalTransport = key
						finalClass = classType
						classMatchedFlag = 1
						return finalTransport

		return "all"		
	else:
		return "all"

def WeightIdentifier(query,category,ner_list,extendedNERAnalyzedParse):
    if(ner_weight.existWeight(query)):
		weight_terms = ner_weight.getWeights(extendedNERAnalyzedParse)
		for terms in weight_terms:
			ner_list[terms] = weightMarker
		return ner_list
    #else:
	#	print "No WEIGHT exists in the given query"

def AmountIdentifier(query,category,ner_list,extendedNERAnalyzedParse):
	if(ner_amount.existsAmount(query)): 	
		amount_terms = ner_amount.getAmounts(extendedNERAnalyzedParse)
		for terms in amount_terms:
			ner_list[terms] = amountMarker
		return ner_list
	else:
		ner_amount.checkAmountWithoutUnit(extendedNERAnalyzedParse)

    #else:
	#	print "No AMOUNT exists in the given query"
	
def TrainQuotaIdentifier(query,category,ner_list,extendedNERAnalyzedParse):
    if(ner_train_quota.tatkalbooking(query,extendedNERAnalyzedParse)):
		ner_list['tatkal'] = trainQuotaMarker

    #else:
	#	print "No TRAIN QUOTA exists in the given query"

def NumSeatsIdentifier(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF):
	ner_num_seats.getNumSeats(extendedNERAnalyzedParse,last_requested_DF)

def NumStopsIdentifier(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF):
	ner_num_stops.getNumStops(extendedNERAnalyzedParse)

def NumResultsIdentifier(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF):
	ner_num_results.getNumResults(extendedNERAnalyzedParse)


def TravelTypeIdentifier(query,category,ner_list,extendedNERAnalyzedParse,last_requested_DF):
	ner_travel_type.TravelType(extendedNERAnalyzedParse,last_requested_DF)

def SeatPreferenceIdentifier(query,category,transport,ner_list,extendedNERAnalyzedParse):
	if(ner_seat_preference.existsSeatPreference(query)):
#		print "Class exists"
		seed = ner_seat_preference.loadSeatSeedlist(transport)

		bypassTransportFlag = 0
		if(transport == "all"):
			bypassTransportFlag = 1

		# Transport and Class identified by extended NER
		finalTransport = ""
		finalSeat = ""

		seatMatchedFlag = 0
		for key in seed:
			if(transport == key or bypassTransportFlag == 1):
				for seatType in seed[key]:
					seatTypePatterns = ner_seat_preference.loadSeatTypePatterns(key,seatType)
					if(ner_seat_preference.matchedSeat(query,seatType,seatTypePatterns,extendedNERAnalyzedParse)):
						finalTransport = key
						finalSeat = seatType
						seatMatchedFlag = 1
						return
	return

def updateRangeInNER(extendedNERAnalyzedParse):
	range_handler.updateRangeInNER(extendedNERAnalyzedParse)

def timeNormalier(extendedNERAnalyzedParse):
	time_normalizer.normalizeTime(extendedNERAnalyzedParse)
	
