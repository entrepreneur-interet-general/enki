from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from datetime import datetime
from enum import Enum

from typing import List

from ...entities.event_entity import EventEntity


class TaskType(Enum):
    ASK = 1
    DO = 2
    NEED_INFO = 3


@dataclass
class TaskEntity(EventEntity):
    event_type: str = field(default="task")
    task_type: TaskType = field(default_factory=lambda: None)
    executor_id: str = field(default_factory=lambda: None)
    executor_type: str = field(default_factory=lambda: None)
    #user_ids: str = field(default_factory=list)
    done_at: datetime = field(default_factory=lambda: None)
    tags: List = field(default_factory=lambda: [])

    def __eq__(self, other):
        return self.uuid == other.uuid

