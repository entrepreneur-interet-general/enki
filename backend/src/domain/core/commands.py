from uuid import uuid4

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Coroutine

from domain.affairs.entities.affair_entity import AffairEntity
from domain.core.topics import AffairCreatedTopic, Topic

EventCallback = Callable[[Any], Coroutine[Any, Any, Any]]


@dataclass
class Command:
    data: Any
    topic: Topic

    def __post_init__(self):
        self.uuid: str = str(uuid4())
        self.timestamp: datetime = datetime.now()
