from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from domain.tasks.entities.message_entity import MessageEventEntity


@dataclass_json
@dataclass
class InformationEntity(MessageEventEntity):
    tags: List = field(default_factory=lambda: [])

