from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

from typing import Union, Optional

from werkzeug.exceptions import HTTPException

from domain.core.entity import Entity
from enum import Enum

from domain.users.entities.user import UserEntity


class EvenementClosedException(HTTPException):
    code = 410
    description = "Evenement is closed"


class EvenementType(str, Enum):
    NATURAL = "natural"
    RASSEMBLEMENT = "rassemblement"


@dataclass_json
@dataclass
class EvenementEntity(Entity):
    """

    """
    title: str
    description: Union[str, None]
    type: EvenementType
    started_at: datetime
    creator_id: Optional[str] = field(default_factory=lambda: None)
    creator: UserEntity = field(default_factory=lambda: None)
    ended_at: Union[datetime, None] = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    @property
    def closed(self):
        return self.ended_at and self.ended_at < datetime.now()

    def check_can_assign(self):
        if self.closed:
            raise EvenementClosedException
