from datetime import datetime
from uuid import uuid4

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import List
import xml.dom.minidom
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.entities.sge.sge_enums import SgeMessageTypeEnum


@dataclass
class SgeMessageEntity(DataClassJsonMixin):
    id: uuid4
    emetteur: str
    type: SgeMessageTypeEnum
    destinataires: List[str]
    date_emission: datetime
    message_brut: str

    @property
    def affair(self) -> AffairEntity:
        return AffairEntity.from_xml(xml.dom.minidom.parseString(self.message_brut))
