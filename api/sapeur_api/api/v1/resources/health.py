from flask_restful import Resource


class HealthResource(Resource):

    def get(self):
        return {"msg": "api is running fine !"}, 200
