from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum

from typing import Union, List, Optional

from domain.core.entity import Entity
from domain.evenements.entity import EvenementEntity
from domain.messages.entities.resource import ResourceEntity
from domain.messages.entities.tag_entity import TagEntity
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

    def assign_evenement(self, evenement: EvenementEntity):
        evenement.check_can_assign()
        self.evenement_id = evenement.uuid

    def add_tag(self, tag: TagEntity) -> None:
        self.tags.append(tag)

    def remove_tag(self, tag: TagEntity) -> None:
        self.tags.remove(tag)

    def add_resource(self, resource: ResourceEntity) -> None:
        self.resources.append(resource)
        resource.set_message_id(self.uuid)

    def remove_resource(self, resource: ResourceEntity) -> None:
        self.resources.remove(resource)
        resource.reset_message_id()

    def set_creator(self, user: UserEntity):
        self.creator = user