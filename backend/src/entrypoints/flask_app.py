from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from entrypoints import views
from service_layer.messagebus import HANDLERS
from .config import SapeursConfig
from .extensions import event_bus, api_spec
from .errors import errors


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

    api = Api(app, errors=errors)
    context = app.config["CONTEXT_FACTORY"](config=SapeursConfig())
    configure_event_bus(context=context)
    context.init_app(app=app)
    configure_apispec(app=app)
    register_blueprints(app)
    return app


def configure_event_bus(context):
    for topic, callbacks in HANDLERS.items():
        for callback in callbacks:
            event_bus.subscribe(topic=topic, callback=callback)


app = create_app()
