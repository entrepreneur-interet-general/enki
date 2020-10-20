from flask import Flask, make_response, request
from flask.json import jsonify
from flask_restful import Api
from adapters.csv.csv_scheduled_event_bus import CsvScheduledEventBus

from entrypoints.repositories import Repositories
from entrypoints.task_ressource import TaskListResource, TaskResource
from heplers.clock import RealClock
from entrypoints.affair_ressource import AffairListResource
from entrypoints.config import SapeursConfig

app = Flask('sapeurs')
app.config.from_object(SapeursConfig)

api = Api(app)
repositories = Repositories()


@app.route('/')
def hello_sapeurs():
    response = make_response(jsonify({'message': 'Hello, Sapeurs!'}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


api.add_resource(TaskListResource, '/tasks', resource_class_kwargs={'taskRepo': repositories.task})
api.add_resource(TaskResource, '/tasks/<uuid>', resource_class_kwargs={'taskRepo': repositories.task})

clock = RealClock()
csv_path = 'tests/integration/temp_data/events_to_dispatch.csv'
event_bus = CsvScheduledEventBus(clock=clock, csv_path=csv_path)
event_bus.subscribe(topic='vehicule_changed_status', callback=lambda e: print(e))
event_bus.start_and_play(time_step=1., speed=20, resync=False)

api.add_resource(AffairListResource, '/affairs', resource_class_kwargs={'affairRepo': repositories.affairs})
