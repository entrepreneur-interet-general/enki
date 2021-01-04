from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum

from typing import List, Union

from domain.tasks.entities.message_entity import MessageEventEntity


class TaskType(str, Enum):
    ASK = "ask"
    DO = "do"
    NEED_INFO = "need_info"
    UNKNOWN = "unknown"


@dataclass_json
@dataclass
class TaskEntity(MessageEventEntity):
    type: TaskType = field(default_factory=lambda: TaskType.UNKNOWN)
    executor_id: Union[str, None] = field(default_factory=lambda: None)
    #executor_type: Union[str, None] = field(default_factory=lambda: None)
    done_at: Union[datetime, None] = field(default_factory=lambda: None)
    tags: List = field(default_factory=lambda: [])

    def __eq__(self, other):
        return self.uuid == other.uuid