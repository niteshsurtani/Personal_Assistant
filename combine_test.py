import os,unittest
import preprocessing_tools.extended_ner.travel.ner_classifier.test_ner_city
from preprocessing_tools.extended_ner.travel.ner_classifier.test_ner_city import suite

unittest.TextTestRunner().run(suite())
