from abc import ABC
from dataclasses import dataclass, field
from uuid import uuid4

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Entity(ABC):
    uuid: str

    def __eq__(self, other):
        return self.uuid == other.uuid
