from typing import Dict
from uuid import uuid4


def message_factory() -> Dict[str, str]:
    message = {
        "uuid": str(uuid4()),
        "title": "My other e2e title",
        "description": "My e2e description",
        "evenement_id": "event_id"
    }
    return message
