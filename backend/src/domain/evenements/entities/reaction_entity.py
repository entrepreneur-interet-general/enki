from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Union, Optional

from dataclasses_json import dataclass_json
from slugify import slugify

from domain.core.entity import Entity


class ReactionType(Enum, str):
    LOOKING = 'looking'
    OK = 'ok'
    ON_MY_WAY = 'on_my_way'
    NICELY_DONE = 'nicely_done'


@dataclass_json
@dataclass
class ReactionEntity(Entity):
    type: ReactionType
    creator_id: str = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
