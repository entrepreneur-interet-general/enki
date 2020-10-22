from flask import Blueprint, make_response, jsonify
from flask_restful import Api

enki_blueprint = Blueprint(name="enki_blueprint", import_name=__name__, url_prefix="/api/enki")
api = Api(enki_blueprint)


@enki_blueprint.route('/', methods=["GET"])
def hello_enki():
    response = make_response(jsonify({'message': 'Hello, Enki!'}))
    return response
