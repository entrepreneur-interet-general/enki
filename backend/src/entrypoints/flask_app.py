from flask import Flask, make_response, jsonify
from flask_restful import Api
from flask_cors import CORS
from entrypoints.extensions import api_spec
from typing import List
from domain.affairs.entities.sge.sge_message_entity import SgeMessageEntity
from entrypoints.config import SapeursConfig
from entrypoints import views
from .extensions import repositories


def register_blueprints(app: Flask):
    """
    Register blueprints
    :param app:
    :return:
    """
    app.register_blueprint(views.couvops_blueprint)
    app.register_blueprint(views.hello_page_blueprint)
    app.register_blueprint(views.enki_blueprint)
    app.register_blueprint(views.enki.enki_blueprint_v1)
    app.register_blueprint(views.core_blueprint)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    api_spec.init_app(app)


def create_app():
    """

    :return:
    """
    app = Flask('sapeurs')
    app.config.from_object(SapeursConfig)
    CORS(app)

    api = Api(app)
    configure_apispec(app=app)
    register_blueprints(app)
    return app


app = create_app()

@app.route('/events')
def get_events():
    all_messages: List[SgeMessageEntity] = repositories.message.get_all()
    response = make_response(jsonify({'messages': [msg.affair.to_json() for msg in all_messages]}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response