from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List

from domain.tasks.entities.message_entity import MessageEventEntity


@dataclass_json
@dataclass
class InformationEntity(MessageEventEntity):
    pass
