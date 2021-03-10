from apispec import APISpec, BasePlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import jsonify, render_template, Blueprint

from .plugin import FlaskRestfulPlugin


class APISpecExt:
    """Very simple and small extension to use apispec with this API as a flask extension
    """

    def __init__(self, app=None, **kwargs):
        self.spec = None

        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        app.config.setdefault("APISPEC_TITLE", "enki_api")
        app.config.setdefault("APISPEC_VERSION", "4.0.0")
        app.config.setdefault("OPENAPI_VERSION", "3.0.3")
        app.config.setdefault("SWAGGER_JSON_URL", "/swagger.json")
        app.config.setdefault("SWAGGER_UI_URL", "/documentation")
        app.config.setdefault("SWAGGER_URL_PREFIX", None)

        self.spec = APISpec(
            title=app.config["APISPEC_TITLE"],
            version=app.config["APISPEC_VERSION"],
            openapi_version=app.config["OPENAPI_VERSION"],
            plugins=[FlaskRestfulPlugin(), MarshmallowPlugin(), DisableOptionsOperationPlugin()],
            **kwargs
        )

        blueprint = Blueprint(
            "swagger",
            __name__,
            template_folder="./templates",
            url_prefix=app.config["SWAGGER_URL_PREFIX"],
        )

        blueprint.add_url_rule(
            app.config["SWAGGER_JSON_URL"], "swagger_json", self.swagger_json
        )
        blueprint.add_url_rule(
            app.config["SWAGGER_UI_URL"], "swagger_ui", self.swagger_ui
        )

        blueprint.add_url_rule(
            "/redoc", "redoc_ui", self.redoc_ui
        )

        app.register_blueprint(blueprint)

    def swagger_json(self):
        return jsonify(self.spec.to_dict())

    def swagger_ui(self):
        return render_template("swagger.j2")

    def redoc_ui(self):
        return render_template("redoc.html")

class DisableOptionsOperationPlugin(BasePlugin):

    def operation_helper(self, operations, **kwargs):
        # flask-apispec auto generates an options operation, which cannot handled by apispec.
        # apispec.exceptions.DuplicateParameterError: Duplicate parameter with name body and location body
        # => remove
        operations.pop("options", None)
