from dataclasses import dataclass, field
from .base_entity import BaseEntity
from enum import Enum


class GroupType(Enum):
    SECOURS = 1
    MAIRIE = 2
    PREFECTURE = 3
    COZ = 4
    COGIC = 5
    CIC = 6


@dataclass
class GroupEntity(BaseEntity):
    title: str = field(default_factory=lambda: None)
    description: str = field(default_factory=lambda: None)
    creator_id: str = field(default_factory=lambda: None)
    type: GroupType = field(default_factory=lambda: None)
