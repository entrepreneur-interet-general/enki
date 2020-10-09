from typing import Dict
from flask.testing import FlaskClient
import json

from sqlalchemy import create_engine
from sqlalchemy.sql.schema import MetaData
from entrypoints.flask_app import app, repositories

def test_hello_sapeurs_returns_200_and_expected_message():
  with app.test_client() as client:
    response = client.get('/')
    body = json.loads(response.data)
    print("response data : ", json.loads(response.data))
    assert response.status_code == 200
    assert body['message'] == "Hello, Sapeurs!"

def test_add_task_then_recovers_it_and_recovers_all():
  with app.test_client() as client:
    client: FlaskClient
    
    # adding a task
    task1 = {
      "uuid": "uuid_1",
      "title": "My e2e title"
    }
    add_task_response = post_add_task(client, task1)

    assert add_task_response.status_code == 201
    assert add_task_response.json['message'] == "Success"

    # fetching added task
    fetched_task1_response = client.get("/tasks/" + task1["uuid"])
    assert fetched_task1_response.status_code == 200
    assert fetched_task1_response.json == task1
    
    # adding extra task
    task2 = {
      "uuid": "uuid_2",
      "title": "My other e2e title"
    }
    post_add_task(client, task2)

    # fetching all tasks
    fetched_all_tasks_response = client.get("/tasks")
    assert fetched_all_tasks_response.status_code == 200
    assert fetched_all_tasks_response.json == [task1, task2]

def post_add_task(client: FlaskClient, body: Dict[str, str]):
  return client.post('/tasks', json=body)

