import os
from flask import Flask, make_response, request
from flask.json import jsonify
from adapters.task_repository.sql.orm import start_mappers
from adapters.task_repository.sql.sql_task_repository import SqlTaskRRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.task_repository.task_repository import InMemoryTaskRepository

from service_layer.task_service import add_task, list_tasks


app = Flask('sapeurs')

# repo = InMemoryTaskRepository()
# <<<<<----- TODO move in config file

session_factory = sessionmaker(bind=create_engine(
    os.environ.get('SQLALCHEMY_ENGINE_OPTIONS', 'postgresql://postgres:pg-password@localhost:5432/sapeurs-dev'),
    isolation_level="REPEATABLE READ",
))
session = session_factory()

repo = SqlTaskRRepository(session)
start_mappers()

# ------>>>>>

@app.route('/')
def hello_sapeurs():
	response = make_response(jsonify({'message': 'Hello, Sapeurs!'}))
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

@app.route('/tasks', methods = ['POST'])
def add_task_route():
	add_task(request.json["title"], repo=repo)
	response = make_response('OK', 201)
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

@app.route('/tasks', methods = ['GET'])
def list_tasks_route():
	tasks_list = list_tasks(repo)
	response = make_response(jsonify(tasks_list))
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response