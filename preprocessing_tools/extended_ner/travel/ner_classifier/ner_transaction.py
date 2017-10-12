import os

from PATH_CONSTANTS import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *

from preprocessing_tools.extended_ner.travel.api.transaction import *
from utilities.match_longest_string import *

import logging
import nlp_logging
from nlp_logging import logger

def getTransaction(extendedNERAnalyzedParse):

	'''
	(Object) -> Object

	Takes the NER Parse as input and annotates the transaction request.

	INPUT: booking, cancel, status
	OUTPUT: book, cancel, status

	'''

	logger.info("ENTERING TRANSACTION IDENTIFICATION MODULE")

	for key in extendedNERAnalyzedParse.keys():   
		word = extendedNERAnalyzedParse[key]["word"]
		lemma = extendedNERAnalyzedParse[key]["lemma"]
		
		transaction = getTransactionItems(lemma)
		if transaction:
			annotateParse(extendedNERAnalyzedParse,key,transaction,transaction,transactionMarker)
			logger.debug("Transaction Identified = '%s' from word = '%s'", transaction, word)

	logger.info("TRANSACTION IDENTIFICATION DONE")
