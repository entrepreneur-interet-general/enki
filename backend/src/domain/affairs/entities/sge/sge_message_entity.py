from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import List
from xml.dom import minidom

from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.entities.sge.sge_enums import SgeMessageTypeEnum


@dataclass
class SgeMessageEntity(DataClassJsonMixin):
    id: str
    emetteur: str
    type: SgeMessageTypeEnum
    destinataires: List[str]
    date_emission: datetime
    message_brut: str

    @property
    def affair(self) -> AffairEntity:
        return AffairEntity.from_xml(minidom.parseString(self.message_brut))
