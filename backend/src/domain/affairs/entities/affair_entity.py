from dataclasses import dataclass
from dataclasses_json import dataclass_json
from cisu.entities.cisu_entity import CreateEvent


@dataclass_json
@dataclass
class AffairEntity(CreateEvent):
    """

    """
    location: dict

    def __post_init__(self):
        if self.location is None:
            self.location = {
                "lat": self.eventLocation.coord.lat,
                "lon": self.eventLocation.coord.lon
            }

    @property
    def uuid(self):
        return self.eventId
