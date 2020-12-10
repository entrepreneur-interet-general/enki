from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime

from domain.core.entity import Entity
from domain.core.timestamped import TimeStamped
from enum import Enum


class EvenementType(str, Enum):
    NATURAL = "natural"
    RASSEMBLEMENT = "rassemblement"


@dataclass_json
@dataclass
class EvenementEntity(Entity, TimeStamped):
    """

    """
    title: str
    description: str
    type: EvenementType
    started_at: datetime
    creator_id: str
    ended_at: datetime = None
