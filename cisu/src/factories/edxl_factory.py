from .cisu_factory import CisuEntityFactory
from .factory import Factory
from .uid_factory import UidFactory
from .. import EdxlEntity


class EdxlMessageFactory(Factory):
    def build(self) -> EdxlEntity:
        return EdxlEntity(
            distributionID=UidFactory().build(),
            senderID=UidFactory().build(),
            dateTimeSent=self.clock_seed.generate(),
            dateTimeExpires=self.clock_seed.generate(),
            distributionStatus="status",
            distributionKind="kind",
            resource=CisuEntityFactory().build(),
        )
