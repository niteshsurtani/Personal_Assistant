from flask import Flask
from flask import request
from flask import jsonify
# import genie_nlp
app = Flask(__name__)

@app.route('/hello')
def world():
	return jsonify(hello='world')

@app.route("/", methods=['POST'])
def jarvis():
	data = request.get_json()
	category = data['category']
	query = data['query']
	user_id = data['user_id']

	# dictionary = genie_nlp.nlp_preprocessing_module(category, query, user_id)

	# return jsonify(source=dictionary['source'], destination=destination)
	return jsonify(query=query, category=category)

if __name__ == "__main__":
    app.run()