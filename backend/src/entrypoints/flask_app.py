from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from entrypoints.extensions import api_spec
from typing import List
from domain.affairs.entities.sge.sge_message_entity import SgeMessageEntity
from entrypoints import views
from .config import SapeursConfig


def register_blueprints(app: Flask):
    """
    Register blueprints
    :param app:
    :return:
    """
    app.register_blueprint(views.hello_page_blueprint)
    app.register_blueprint(views.enki_blueprint)
    app.register_blueprint(views.enki.enki_blueprint_v1)
    app.register_blueprint(views.core_blueprint)
    app.register_blueprint(views.echanges_blueprint)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    api_spec.init_app(app)


def create_app(testing=False):
    """

    :return:
    """
    app = Flask('sapeurs')
    app.config.from_object(SapeursConfig)
    CORS(app)

    if testing is True:
        app.config["TESTING"] = True

    api = Api(app)
    context = app.config["CONTEXT_FACTORY"](config=SapeursConfig())
    context.init_app(app=app)
    configure_apispec(app=app)
    register_blueprints(app)
    return app


app = create_app()
