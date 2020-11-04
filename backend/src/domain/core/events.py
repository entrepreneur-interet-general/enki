from uuid import uuid4

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Coroutine

from domain.affairs.entities.affair_entity import AffairEntity
from domain.core.topics import AffairCreatedTopic, AffairReceivedTopic, Topic
from entrypoints.extensions import clock

EventCallback = Callable[[Any], Coroutine[Any, Any, Any]]


@dataclass
class Event:
    uuid: str
    timestamp: datetime
    data: Any
    topic: Topic

    def __post_init__(self):
        self.uuid = str(uuid4())
        self.timestamp = clock.get_now()


@dataclass
class AffairCreatedEvent(Event):
    data: AffairEntity
    topic: Topic = AffairCreatedTopic