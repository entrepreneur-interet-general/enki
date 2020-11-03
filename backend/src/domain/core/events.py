from dataclasses import dataclass
from datetime import date
from typing import Optional
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import Any, Callable, Coroutine, Optional

from domain.core.topics import AffairCreatedTopic, Topic

EventCallback = Callable[[Any], Coroutine[Any, Any, Any]]


@dataclass
class Event:
    uuid: str
    timestamp: datetime
    topic: Topic
    data: Optional[Any] = None


@dataclass_json
@dataclass
class AffairCreatedEvent(Event):
    topic: Topic = AffairCreatedTopic
