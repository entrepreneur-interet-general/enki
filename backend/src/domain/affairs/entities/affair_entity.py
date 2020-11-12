from dataclasses import dataclass
from dataclasses_json import dataclass_json
from domain.affairs.cisu.entities.cisu_entity import CreateEvent


@dataclass_json
@dataclass
class AffairEntity(CreateEvent):
    """

    """

    @property
    def uuid(self):
        return self.eventId


