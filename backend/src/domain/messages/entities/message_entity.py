from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum

from typing import Union, List, Optional

from domain.core.entity import Entity
from domain.users.entities.user import UserEntity


class Severity(Enum):
    EXTREME = 1
    SEVERE = 2
    MODERATE = 3
    MINOR = 4
    UNKNOWN = 5


class MessageType(str, Enum):
    INFORMATION = "info"
    ASK = "ask"
    DO = "do"
    NEED_INFO = "need_info"
    UNKNOWN = "unknown"

    def __str__(self):
        return self.value

@dataclass_json
@dataclass
class MessageEntity(Entity):
    title: str
    description: str
    evenement_id: str
    creator_id: Optional[str] = field(default_factory=lambda: None)
    creator: UserEntity = None
    severity: Severity = field(default_factory=lambda: Severity.UNKNOWN)
    started_at: Union[datetime, None] = field(default_factory=lambda: None)
    tags: List = field(default_factory=lambda: [])
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
    type: MessageType = field(default_factory=lambda: MessageType.UNKNOWN)
    executor_id: Union[str, None] = field(default_factory=lambda: None)
    done_at: Union[datetime, None] = field(default_factory=lambda: None)

    def __eq__(self, other):
        return self.uuid == other.uuid
