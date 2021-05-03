from __future__ import annotations
from uuid import uuid4

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Union, List, Optional

from dataclasses_json import dataclass_json
from werkzeug.exceptions import HTTPException

from domain.core.entity import Entity
from domain.evenements.entities.resource import ResourceEntity
from domain.evenements.entities.tag_entity import TagEntity
from domain.users.entities.user import UserEntity



class ReactionType(str, Enum):
    LOOKING = "looking"
    OK = "ok"
    WELL_DONE = "well-done"
    NO = "no"

    def __str__(self):
        return self.value

@dataclass_json
@dataclass
class ReactionEntity(Entity):
    type: ReactionType
    creator_id: str
    message_id: str
    creator: UserEntity = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.now())

    def __eq__(self, other):
        return self.uuid == other.uuid