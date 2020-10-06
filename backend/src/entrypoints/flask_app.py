from flask import Flask, make_response, request
from flask.json import jsonify

from entrypoints.repositories import Repositories
from domain.tasks.task_service import add_task, get_by_uuid, list_tasks


app = Flask('sapeurs')
repositories = Repositories()

@app.route('/')
def hello_sapeurs():
	response = make_response(jsonify({'message': 'Hello, Sapeurs!'}))
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

@app.route('/tasks', methods = ['POST'])
def add_task_route():
	add_task(request.json["uuid"], request.json["title"], repo=repositories.task)
	response = make_response('OK', 201)
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

@app.route('/tasks', methods = ['GET'])
def list_tasks_route():
	tasks = list_tasks(repositories.task)

	response = make_response(jsonify(tasks))
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

@app.route('/tasks/<uuid>', methods = ['GET'])
def get_task_route(uuid: str):
	task = get_by_uuid(uuid, repositories.task)

	response = make_response(jsonify(task))
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response
