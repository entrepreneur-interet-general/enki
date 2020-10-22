from adapters.csv.csv_scheduled_event_bus import CsvScheduledEventBus

from flask import Blueprint, make_response, jsonify
from flask_restful import Api

from entrypoints.extensions import clock

couvops_blueprint = Blueprint(name="couvops_blueprint", import_name=__name__, url_prefix="/api/couvops")
api = Api(couvops_blueprint)


@couvops_blueprint.route('/', methods=["GET"])
def hello_couvops():
    response = make_response(jsonify({'message': 'Hello, CouvOps!'}))
    return response

# csv_path = 'tests/integration/temp_data/events_to_dispatch.csv'
# event_bus = CsvScheduledEventBus(clock=clock, csv_path=csv_path)
# event_bus.subscribe(topic='vehicule_changed_status', callback=lambda e: print(e))
# event_bus.start_and_play(time_step=1., speed=20, resync=False)
