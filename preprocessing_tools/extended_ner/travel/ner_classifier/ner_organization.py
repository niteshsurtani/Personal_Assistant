from FILE_CONSTANTS import *
from preprocessing_tools.extended_ner.travel.api.organization import *
from utilities.match_longest_string import *
from preprocessing_tools.CATEGORY_LABEL_CONSTANTS import *

import logging
import nlp_logging
from nlp_logging import logger

def findOrganization(extendedNERAnalyzedParse):
	'''
	(Object) -> Object

	Takes the NER Parse as input and annotates the Organization corresponding
	to the Organization at each Organization token.
	The Organization list is loaded from the database matching the first token of Organization name.

	INPUT: Indigo, spicejet, mumbai
	OUTPUT: Indigo, spicejet, no

	'''

	logger.info("ENTERING ORGANIZATION IDENTIFICATION MODULE")

	ner_organization = []

	for key in extendedNERAnalyzedParse.keys():   
		if extendedNERAnalyzedParse[key]["POS"] in ["NN","NNP","JJ"]:
			token = extendedNERAnalyzedParse[key]["word"]
			matched_organization = findOrganizationByName(token)
			for organization_tuple in matched_organization:
				organization = organization_tuple[1]
				if matchLongestString(extendedNERAnalyzedParse,key,organization):
					annotateParse(extendedNERAnalyzedParse,key,organization,organization,organizationMarker)
					ner_organization.append(organization)
					logger.debug("Organization Identified = '%s' with code = '%s'", organization, organization)

	logger.info("ORGANIZATION IDENTIFICATION DONE")
	return ner_organization
	