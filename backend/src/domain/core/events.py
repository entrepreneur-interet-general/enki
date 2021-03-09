from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Coroutine
from uuid import uuid4

from domain.affairs.entities.affair_entity import AffairEntity
from domain.core.topics import AffairCreatedTopic, Topic, CreateUserTopic
from domain.users.entities.user import UserEntity

EventCallback = Callable[[Any], Coroutine[Any, Any, Any]]


@dataclass
class Event:
    data: Any
    topic: Topic

    def __post_init__(self):
        self.uuid: str = str(uuid4())
        self.timestamp: datetime = datetime.now()


@dataclass
class AffairCreatedEvent(Event):
    data: AffairEntity
    topic: Topic = AffairCreatedTopic


@dataclass
class UserCreatedEvent(Event):
    data: UserEntity
    topic: Topic = CreateUserTopic
