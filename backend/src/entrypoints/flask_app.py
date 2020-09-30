from flask import Flask, jsonify, make_response

app = Flask('sapeurs')

@app.route('/')
def hello_sapeurs():
		resp = make_response(jsonify({'message': 'Hello, Sapeurs!'}))
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp
