from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum

from typing import Union, List, Optional

from werkzeug.exceptions import HTTPException

from domain.core.entity import Entity
from domain.evenements.entities.evenement_entity import EvenementEntity
from domain.evenements.entities.resource import ResourceEntity
from domain.evenements.entities.tag_entity import TagEntity
from domain.users.entities.user import UserEntity


class NotFoundResourceInThisMessage(HTTPException):
    code = 404
    description = "Resource not found in this message"


class NotFoundTagInThisMessage(HTTPException):
    code = 404
    description = "Tag not found in this message"


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
    tags: List[TagEntity] = field(default_factory=lambda: [])
    resources: List[ResourceEntity] = field(default_factory=lambda: [])
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

    def add_tag(self, tag: TagEntity) -> TagEntity:
        self.tags.append(tag)
        return tag

    def remove_tag(self, tag: TagEntity) -> TagEntity:
        self.tags.remove(tag)
        return tag

    def get_tags(self) -> List[TagEntity]:
        return self.tags

    def get_tag_by_id(self, uuid: str) -> TagEntity:
        matches = [tag for tag in self.tags if tag.uuid == uuid]
        if not matches:
            raise NotFoundTagInThisMessage()
        return matches[0]

    def add_resource(self, resource: ResourceEntity) -> ResourceEntity:
        self.resources.append(resource)
        resource.set_message_id(self.uuid)
        return resource

    def remove_resource(self, resource: ResourceEntity) -> ResourceEntity:
        self.resources.remove(resource)
        resource.reset_message_id()
        return resource

    def get_resources(self):
        return self.resources

    def get_resource_by_id(self, uuid: str) -> ResourceEntity:
        matches = [resource for resource in self.resources if resource.uuid == uuid]
        if not matches:
            raise NotFoundResourceInThisMessage()
        return matches[0]

    def set_creator(self, user: UserEntity):
        self.creator = user
