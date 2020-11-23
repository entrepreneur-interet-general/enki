from flask_restful import Resource


class HealthResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - core
    """

    def get(self):
        return {"ok": "ok"}