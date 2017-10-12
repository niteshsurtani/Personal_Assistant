from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
import json
import nlp_preprocessing_engine
import search
import time
import logging
from datetime import date
import os.path
import nlp_logging
from nlp_logging import loggingHandler
from nlp_logging import logger
import newrelic.agent


app = Flask(__name__)

@app.route("/nlp", methods=['POST'])
def nlp():
	directory = "logs/"
	today = date.today()
	todayString = today.isoformat()
	
	if not os.path.isfile(directory + todayString):
		os.system("touch " + directory + todayString)
		loggingHandler = logging.FileHandler(directory + todayString)
		logger.addHandler(loggingHandler)

	data = request.get_json()

	category = data['category']
	query = data['query']
	
	last_requested_df = ""
	if 'last_requested_df' in data and data['last_requested_df']:
		last_requested_df = data['last_requested_df'].lower()

	# Logging INFO
	logger.info("ENTERING NLP ENGINE")
	logger.debug(data)
	logger.info("\n")

	analyzedDF = nlp_preprocessing_engine.preprocessor(query,category,last_requested_df)
	return json.dumps(analyzedDF)







@app.route("/df_checker", methods=['POST'])
def df():
	# Input: Analyzed DF
	# Output: Is DF complete
	data = request.get_json()

	isCompleteDF = df_checker.check(data)
	return isCompleteDF

@app.route("/generator", methods=['POST'])
def generator():
	# Input: Hierarchial DFs in priority, what to generator as null
	# Output: Next question
	data = request.get_json()

	generatedQuestion = generator.generate(data)
	return generatedQuestion

@app.route("/search", methods=['POST'])
def searchRest():
	# Input: Complete list of mandatory and optional DFs
	# Output: List of matching restaurants

	frame = request.get_json()

	searchResults = search.findFlight()
	# print searchResults
	return json.dumps(searchResults)




if __name__ == "__main__":
	newrelic.agent.initialize('newrelic.ini')
	app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)

