import os

from PATH_CONSTANTS import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *

from preprocessing_tools.extended_ner.travel.api.transport import *
from utilities.match_longest_string import *

import logging
import nlp_logging
from nlp_logging import logger

def getTransport(extendedNERAnalyzedParse):

	'''
	(Object) -> Object

	Takes the NER Parse as input and annotates the transport type.

	INPUT: flight, air, bus, rail
	OUTPUT: flight, flight, bus, train

	'''

	logger.info("ENTERING TRANSPORT IDENTIFICATION MODULE")

	for key in extendedNERAnalyzedParse.keys():   
		word = extendedNERAnalyzedParse[key]["word"]
		lemma = extendedNERAnalyzedParse[key]["lemma"]
		
		transport = getTransportItems(lemma)
		if transport:
			annotateParse(extendedNERAnalyzedParse,key,transport,transport,transportMarker)
			logger.debug("Transport Identified = '%s' from word = '%s'", transport, word)

	logger.info("TRANSPORT IDENTIFICATION DONE")
