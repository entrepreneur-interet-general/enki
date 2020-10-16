from dataclasses import dataclass
from dataclasses_json import dataclass_json

from domain.core.timestamped import TimeStamped
from domain.core.entity import Entity
from enum import Enum


class GroupType(Enum):
    SECOURS = 1
    MAIRIE = 2
    PREFECTURE = 3
    COZ = 4
    COGIC = 5
    CIC = 6

@dataclass_json
@dataclass
class GroupEntity(Entity, TimeStamped):
    title: str
    description: str
    creator_id: str
    type: GroupType
