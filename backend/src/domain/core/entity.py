from abc import ABC
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from .timestamped import TimeStamped


@dataclass_json
@dataclass
class Entity(ABC):
    uuid: str

    def __eq__(self, other):
        return self.uuid == other.uuid


@dataclass_json
@dataclass
class TimeStampedEntity(Entity, TimeStamped):
    """

    """
