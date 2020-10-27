import pathlib

from .factory import Factory
from ..constants.constants import RiskThreatConstants, HealthMotiveConstants, \
    LocationKindConstants, WhatsHappenConstants
from ..entities.alert_entity import AlertCode
from ..entities.commons.common_alerts import Version, WhatsHappen, LocationKind, \
    RiskThreat, HealthMotive, Victims, Count, MainVictim


class WhatsHappenFactory(Factory):
    def generate(self) -> WhatsHappen:
        return HealthMotiveConstants().get_random()


class LocationKindFactory(Factory):
    def generate(self) -> WhatsHappen:
        return LocationKindConstants().get_random()


class RiskThreatFactory(Factory):
    def generate(self) -> WhatsHappen:
        return RiskThreatConstants().get_random(how_many=3)


class HealthMotiveFactory(Factory):
    def generate(self) -> WhatsHappen:
        return HealthMotiveConstants().get_random()


class VictimsFactory(Factory):
    def generate(self) -> Victims:
        return Victims(
            count=Count.random(),
            mainVictim=MainVictim.random(),
            comment=self.faker.text
        )


class AlertCodeFactory(Factory):
    def build(self) -> AlertCode:
        return AlertCode(
            version=Version("latest"),
            whatsHappen=WhatsHappenFactory().generate(),
            locationKind=LocationKindFactory().generate(),
            riskThreat=RiskThreatFactory().generate(),
            healthMotive=HealthMotiveFactory().generate(),
            victims=Victims,
        )
