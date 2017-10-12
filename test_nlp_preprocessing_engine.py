import unittest
from nlp_preprocessing_engine import *
import ast

class NLP_Preprocessing(unittest.TestCase):
	
	def __init__(self, input, output):
		super(NLP_Preprocessing, self).__init__()
		self.input = input
		self.output = output

	def runTest(self):
		self.assertEqual(preprocessor(self.input[0],self.input[1],self.input[2]), self.output)

def suite():
	try:
		suite = unittest.TestSuite()
		test_data = []

		data_file = "data_nlp_preprocessing_engine"
		
		# Reading NERParse and city_output in each line
		with open(data_file) as f:
			content = f.readlines()

		for index in range(0,len(content),2):
			query = content[index].split(';')
			index += 1
			if index < len(content):
				DF = ast.literal_eval(content[index])
				test_data.append((query, DF))

 		suite.addTests(NLP_Preprocessing(input, output) for input, output in test_data)
		return suite
				
	# except Exception as e:
	except:
		print "Error"


if __name__ == '__main__':
	unittest.TextTestRunner().run(suite())
