from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum

from typing import List, Union

from domain.tasks.entities.event_entity import MessageEventEntity


class TaskType(Enum):
    ASK = 1
    DO = 2
    NEED_INFO = 3
    UNKNONW = 4


@dataclass_json
@dataclass
class TaskEntity(MessageEventEntity):
    task_type: TaskType = field(default_factory=lambda: TaskType.UNKNONW)
    event_type: str = field(default="task")
    executor_id: Union[str, None] = field(default_factory=lambda: None)
    executor_type: Union[str, None] = field(default_factory=lambda: None)
    done_at: Union[datetime, None] = field(default_factory=lambda: None)
    tags: List = field(default_factory=lambda: [])
    # user_ids: str = field(default_factory=list)

    def __eq__(self, other):
        return self.uuid == other.uuid