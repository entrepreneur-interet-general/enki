from uuid import uuid4
from datetime import datetime

from domain.evenements.entities.evenement_entity import EvenementType


def make_evenemnt(uuid: str = str(uuid4())):
    return {
        "uuid": uuid,
        "title": "Evenement 1 title",
        "description": "Evenement 1 description",
        "type": EvenementType.NATURAL,
        "started_at": datetime.now(),
        "creator_id": str(uuid4()),
    }
