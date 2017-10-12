import location_disambiguator
import date_disambiguator

from FILE_CONSTANTS import *

def disambiguateCategories(query,category,NERAnalyzedParse,chunkedParse,last_requested_DF):
	last_requested_DF = last_requested_DF.lower()

   	locationList = disambiguateLocations(query,category,NERAnalyzedParse,chunkedParse,last_requested_DF)
   	dateList = disambiguateDates(query,category,NERAnalyzedParse,chunkedParse,last_requested_DF)
 	disambiguatedDF = mergeDictionaries(locationList,dateList)
 	return disambiguatedDF

def disambiguateLocations(query,category,NERAnalyzedParse,chunkedParse,last_requested_DF):
   	locationList = []

	locationList, locationCode = location_disambiguator.getNumberOfLocation(NERAnalyzedParse)
	print locationList

	numLocations = len(locationList)

	disambiguatedLocationList = {}
	if numLocations == 1:
		disambiguatedLocationList  = location_disambiguator.disambiguateLocations(locationList,locationCode,NERAnalyzedParse,chunkedParse,numLocations)
		print "disambiguateLocations = ",
		print disambiguatedLocationList

		if len(disambiguatedLocationList.keys())>0:
			if last_requested_DF in ["source","destination"] and disambiguatedLocationList.keys()[0] != last_requested_DF:
				print "=== CONFLICT ==="
		else:
			if last_requested_DF in ["source","destination"]:
				disambiguatedLocationList[last_requested_DF] = locationCode[locationList[0]]
			else:
				disambiguatedLocationList["source"] = locationCode[locationList[0]]
	elif numLocations == 2:
		disambiguatedLocationList = location_disambiguator.disambiguateLocations(locationList,locationCode,NERAnalyzedParse,chunkedParse,numLocations)
	return disambiguatedLocationList


def disambiguateDates(query,category,NERAnalyzedParse,chunkedParse,last_requested_DF):
	dateList = {}
	
	dateList = date_disambiguator.getNumberOfDates(NERAnalyzedParse,chunkedParse)

	numDates = len(dateList)
	print "DateList = ",
	print dateList

	disambiguatedDateList = {}
	if numDates == 1:
		if last_requested_DF in ['start_date','end_date']:
			disambiguatedDateList[last_requested_DF] = dateList[0]
		else:
			disambiguatedDateList['start_date'] = dateList[0]
		# disambiguatedDateList = date_disambiguator.disambiguateDates(dateList,numDates,chunkedParse)
	elif numDates == 2:
		disambiguatedDateList = date_disambiguator.disambiguateDates(dateList,numDates,chunkedParse)
		disambiguatedDateList["round_trip"] = 1

	print "========= DateList ============="
	print disambiguatedDateList
	return disambiguatedDateList

def mergeDictionaries(locationList,dateList):
	disambiguatedDF = {}
	disambiguatedDF = locationList.copy()
	disambiguatedDF.update(dateList)
	return disambiguatedDF

def printDictionary(dictionary):
	for key,value in dictionary.iteritems():
		if(isinstance(value,dict)):
			print str(key)+"\t",
			for k1,v1 in value.iteritems():
					print str(k1)+ " : "+str(v1),
			print
		else:
			print str(key) + " : " + str(value)

