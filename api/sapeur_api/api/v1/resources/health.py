from flask_restful import Resource
from flask import current_app


class HealthResource(Resource):
    def get(self):
        return {
                   "msg": "api is running fine !",
                   "database_uri": current_app.config["SQLALCHEMY_DATABASE_URI"]
               }, 200
