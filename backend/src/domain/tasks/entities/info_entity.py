from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from domain.tasks.entities.event_entity import MessageEventEntity
from typing import Union, List


@dataclass_json
@dataclass
class InformationEntity(MessageEventEntity):
    event_type: str = field(default="information")
    executor_id: Union[str, None] = field(default_factory=lambda: None)
    executor_type: Union[str, None] = field(default_factory=lambda: None)
    user_ids: List = field(default_factory=list)
