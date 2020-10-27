import pathlib

from .factory import Factory
from ..entities.alert_entity import AlertCode
from ..entities.commons.common_alerts import Version, WhatsHappen, LocationKind,\
    RiskThreat, HealthMotive, Victims

class WhatsHappenFactory(Factory):
    def generate(self)->WhatsHappen:

        return WhatsHappen(
            code=,
            label=,
            comment=self.faker.text,

        )


class AlertCodeFactory(Factory):
    def build(self) -> AlertCode:
        return AlertCode(
            version=Version("latest"),
            whatsHappen=WhatsHappen,
            locationKind=LocationKind,
            riskThreat=[RiskThreat],
            healthMotive=HealthMotive,
            victims=Victims,
        )

