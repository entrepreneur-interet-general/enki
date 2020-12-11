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
        if request.headers['Content-Type'] in ["application/xml", 'text/xml']:
            current_app.logger.info("post message")
            xml = request.data.decode("utf-8")
            AffairService.add_affair(xml, repo=current_app.context.affair)
            return {
                   "msg": "success"
               }, 200
        return {
            "msg": "error",
            "contentType": request.headers['Content-Type']
        }, 200