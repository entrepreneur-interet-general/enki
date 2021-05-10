from flask import current_app, request
from flask_restful import Resource

from domain.affairs.services.affair_service import AffairService
from domain.core.events import AffairCreatedEvent
from domain.echanges.schema.echange import EchangeSchema
from domain.echanges.services.echange_service import EchangeService
from entrypoints.extensions import event_bus


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

            current_app.logger.info(f"xml {xml}")


            echange = EchangeSchema().load({
                'payload':xml
            })
            _ = EchangeService.add_echange(echange, uow=current_app.context)
            affair = AffairService.add_affair_from_xml(xml, uow=current_app.context)
            event_bus.publish(AffairCreatedEvent(data=affair))
            return {
                   "message": "success"
               }, 200
        return {
            "message": "error",
            "contentType": request.headers['Content-Type']
        }, 200
