from typing import Dict
from uuid import uuid4

def tag_factory()-> Dict[str, str]:
    tag = {
        "uuid": str(uuid4()),
        "title": "My other e2e title",
        "description": "My e2e description"
    }
    return tag
