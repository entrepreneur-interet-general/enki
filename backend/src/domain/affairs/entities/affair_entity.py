from dataclasses import dataclass
from dataclasses_json import dataclass_json
from cisu.entities.cisu_entity import CreateEvent


@dataclass_json
@dataclass
class AffairEntity(CreateEvent):
    """

    """
    location: dict = None

    def __post_init__(self):
        if self.location is None:
            if isinstance(self.eventLocation, dict):
                self.location = {
                    "lat": self.eventLocation["coord"]["lat"],
                    "lon": self.eventLocation["coord"]["lon"]
                }
            else:
                self.location = {
                    "lat": self.eventLocation.coord.lat,
                    "lon": self.eventLocation.coord.lon
                }


    @property
    def geom_location(self):
        return f'POINT({self.location["lat"]} {self.location["lon"]})'

    @property
    def uuid(self):
        return self.eventId
