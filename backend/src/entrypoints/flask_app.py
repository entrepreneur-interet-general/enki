from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from sqlalchemy.orm import clear_mappers

from adapters.postgres.orm import start_mappers
from entrypoints import views
from service_layer.messagebus import HANDLERS
from .commands.seeds.group import create_group
from .config import EnkiConfig
from .extensions import event_bus, api_spec
from .errors import errors
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


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
    app = Flask('enki')
    app.config.from_object(EnkiConfig)
    CORS(app)

    if testing is True:
        app.config["TESTING"] = True

    api = Api(app, errors=errors)
    context = app.config["CONTEXT_FACTORY"](config=EnkiConfig())
    configure_event_bus(context=context)
    context.init_app(app=app)
    configure_apispec(app=app)
    register_blueprints(app)
    register_cli_commands(app=app)
    configure_orm()
    return app

def register_cli_commands(app):
    app.cli.add_command(create_group)


def configure_orm():
    clear_mappers()
    start_mappers()


def configure_event_bus(context):
    for topic, callbacks in HANDLERS.items():
        for callback in callbacks:
            event_bus.subscribe(topic=topic, callback=callback)


app = create_app()
