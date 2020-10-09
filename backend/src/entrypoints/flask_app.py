from logging import log
from flask import Flask, make_response, request
from flask.json import jsonify
from flask_restful import Api

from entrypoints.repositories import Repositories
from domain.tasks.task_service import add_task, get_by_uuid, list_tasks
from entrypoints.task_ressource import TaskListResource, TaskResource


app = Flask('sapeurs')
api = Api(app)
repositories = Repositories()

@app.route('/')
def hello_sapeurs():
	response = make_response(jsonify({'message': 'Hello, Sapeurs!'}))
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

api.add_resource(TaskListResource, '/tasks', resource_class_kwargs={'taskRepo': repositories.task})
api.add_resource(TaskResource, '/tasks/<uuid>', resource_class_kwargs={'taskRepo': repositories.task})

