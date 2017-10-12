from flask import Flask
from flask import request
from flask import jsonify

import nlp_preprocessing_engine
#Add a comment to this line
# import genie_nlp
app = Flask(__name__)
'''
@app.route('/hello')
def world():
	return jsonify(hello='world')
'''
@app.route("/nlp", methods=['POST'])
def jarvis():
	query = "I want to biok a Spicejet business clss flight tikket with window seat from hyderabad and to Bangalore leaving on 21st June and return on 25th June with an extra luggage of 15 kg in price range of 10 K to 15 K."
	category = "travel"
	'''
	data = request.get_json()
	category = data['category']
	query = data['query']
	user_id = data['user_id']
'''
	analyzedDF = nlp_preprocessing_engine.preprocessor(query,category)
	print analyzedDF

# return jsonify(source=dictionary['source'], destination=destination)
	return jsonify(query=query, category=category)

if __name__ == "__main__":
	app.run()
