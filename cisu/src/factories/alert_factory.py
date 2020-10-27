from .factory import Factory
from .location_factory import LocationTypeFactory
from ..entities.alert_entity import AlertEntity
from .uid_factory import UidFactory
from cisu.src.entities.commons.common_alerts import Reporting, AlertId, Call, Caller, CallTaker, AnyURI, Language


class CallFactory:
    def build(self) -> Call:
        return Call(
            source="source_test",
            dialledURI=AnyURI("ok:ok")
        )


class CallerFactory(Factory):
    def build(self) -> Caller:
        return Caller(
            callerURI=AnyURI("ok:ok"),
            callbackURI=AnyURI("ok:ok"),
            spokenLanguage=Language("fr_FR"),
            callerInformation=self.faker.text
        )


class CallTakerFactory:
    def build(self) -> CallTaker:
        return CallTaker(
            organization="ansc",
            controlRoom="enki",
            calltakerURI=AnyURI("ok:ok"),
        )


class AlertFactory(Factory):
    def build(self) -> AlertEntity:
        return AlertEntity(
            alertId=AlertId(UidFactory().build()),
            receivedAt=self.clock_seed.generate(),
            reporting=Reporting.random(),
            alertInformation=self.faker.text,
            alertLocation=LocationTypeFactory().build(),
            call=CallFactory().build(),
            caller=CallerFactory().build(),
            callTaker=CallTakerFactory().build(),
            resource=[],
        )

class PrimaryAlertFactory(Factory):
    def build(self) -> AlertEntity:
        return AlertEntity(
            alertId=AlertId(UidFactory().build()),
            receivedAt=self.clock_seed.generate(),
            reporting=Reporting.random(),
            alertInformation=self.faker.text,
            alertLocation=LocationTypeFactory().build(),
            call=CallFactory().build(),
            caller=CallerFactory().build(),
            callTaker=CallTakerFactory().build(),
            resource=[],
        )
