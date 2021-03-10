from domain.evenements.services.evenement_service import EvenementService
from flask import current_app

uow = current_app.context
event_uuid = "29ef5913-258c-4fb9-94d7-4ef94aa081f2"
EvenementService.create_list_of_dict_entries(uuid=event_uuid, uow=uow)