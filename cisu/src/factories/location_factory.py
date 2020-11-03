from .factory import Factory
from cisu.src.entities.commons import LocationType, CoordType
from cisu.src.entities.commons.location_type import LocationShape


class CoordTypeFactory(Factory):
    def build(self):
        lat, lon = self.location_seed.generate()
        return CoordType(lat=lat, lon=lon, height=0)


class LocationTypeFactory(Factory):
    def build(self):
        return LocationType(name="location_name",
                            address=self.faker.address(),
                            coord=CoordTypeFactory().build(),
                            type=LocationShape.POINT)
