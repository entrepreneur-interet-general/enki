from flask import Flask
from flask_restful import Api
from entrypoints.extensions import api_spec
from entrypoints.config import SapeursConfig
from entrypoints import views


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

    api = Api(app)
    configure_apispec(app=app)
    register_blueprints(app)

    return app


app = create_app()
