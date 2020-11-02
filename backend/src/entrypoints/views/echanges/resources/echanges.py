from flask_restful import Resource
from flask import current_app, request

from domain.affairs.services.affair_service import AffairService


class EchangeMessageResource(Resource):
    """Single object resource

    ---
    post:
      tags:
        - echanges
    """

    def post(self):
        if request.headers['Content-Type'] == 'text/xml':
            current_app.logger.info(f"request.data {request.data}")
            current_app.logger.info(f"type(request.data) {type(request.data)}")
            xml = request.data.decode("utf-8")
            current_app.logger.info(f"receive xml data {xml}")
            AffairService.add_affair(xml, repo=current_app.context.affair)
        return {
                   "msg": "success"
               }, 200
