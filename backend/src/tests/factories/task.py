from typing import Dict
from uuid import uuid4

def task_factory()-> Dict[str, str]:
    task = {
        "uuid":str(uuid4()),
        "title": "My other e2e title",
        "description": "My e2e description",
        "evenement_id": "event_id"
    }
    return task
