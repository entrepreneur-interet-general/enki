
from flask import current_app

uow = current_app.context
with uow:
    evenement = uow.evenement.get_by_uuid("evenement_id_10")
    print(evenement.get_all_entries())