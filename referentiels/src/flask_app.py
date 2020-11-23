from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from .entrypoints.extensions import api_spec
from .entrypoints import views
from .config import ReferentielConfig


def register_blueprints(app: Flask):
    """
    Register blueprints
    :param app:
    :return:
    """
    app.register_blueprint(views.referentiels_blueprint)
    app.register_blueprint(views.core_blueprint)
    app.register_blueprint(views.hello_page_blueprint)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    api_spec.init_app(app)


def create_app(testing=False):
    """

    :return:
    """
    app = Flask('sapeurs')
    app.config.from_object(ReferentielConfig)
    CORS(app)

    if testing is True:
        app.config["TESTING"] = True

    _ = Api(app)
    context = app.config["CONTEXT_FACTORY"](config=ReferentielConfig())
    context.init_app(app=app)
    configure_apispec(app=app)
    register_blueprints(app)
    return app


app = create_app()
