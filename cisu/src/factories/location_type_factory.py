from ..entities.commons import LocationType, CoordType
from .factory import AbstractFactory
from .seed import SeedFactory
from ..entities.commons.location_type import LocationShape


class LocationTypeFactory(AbstractFactory, SeedFactory):
    def generate(self):
        return LocationType(
            name=self.faker.name(),
            address=[self.faker.address()],
            coord=CoordType(lat=self.lat, lon=self.lon, height=10),
            type=LocationShape("POINT")
        )
