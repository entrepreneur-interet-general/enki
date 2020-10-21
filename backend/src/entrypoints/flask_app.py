from flask import Flask, make_response, Blueprint, url_for
from flask.json import jsonify
from flask_restful import Api

from entrypoints.repositories import Repositories
from entrypoints.views.enki.v1.blueprint import enki_v1_blueprint
from heplers.clock import RealClock
from entrypoints.config import SapeursConfig

app = Flask('sapeurs')
app.config.from_object(SapeursConfig)

api = Api(app)
repositories = Repositories()

simple_page = Blueprint('api', __name__, url_prefix="/api/v1")


@simple_page.route('/')
def hello_sapeurs():
    response = make_response(jsonify({'message': 'Hello, Sapeurs!'}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


app.register_blueprint(simple_page)
app.register_blueprint(enki_v1_blueprint)
# api.add_resource(TaskListResource, '/tasks', resource_class_kwargs={'taskRepo': repositories.task})
# api.add_resource(TaskResource, '/tasks/<uuid>', resource_class_kwargs={'taskRepo': repositories.task})

clock = RealClock()


# csv_path = 'tests/integration/temp_data/events_to_dispatch.csv'
# event_bus = CsvScheduledEventBus(clock=clock, csv_path=csv_path)
# event_bus.subscribe(topic='vehicule_changed_status', callback=lambda e: print(e))
# event_bus.start_and_play(time_step=1., speed=20, resync=False)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return {
        "data": links
    }
