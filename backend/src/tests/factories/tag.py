from random import random
from typing import Dict
from uuid import uuid4


def tag_factory() -> Dict[str, str]:
    tag = {
        "uuid": str(uuid4()),
        "title": "My other e2e title" + str(random()),
    }
    return tag
