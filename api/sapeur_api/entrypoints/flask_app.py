from flask import Flask, jsonify

app = Flask('sapeurs')

@app.route('/')
def hello_sapeurs():
	return jsonify({'message': 'Hello, Sapeurs!'}), 200
