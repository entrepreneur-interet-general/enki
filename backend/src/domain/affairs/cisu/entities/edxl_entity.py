from uuid import uuid4

from dataclasses import dataclass

from .cisu_entity import CisuEntity
from .commons import DateType


@dataclass
class EdxlEntity:
    """

    """
    distributionID: uuid4
    senderID: str
    dateTimeSent: DateType
    dateTimeExpires: DateType
    distributionStatus: str
    distributionKind: str
    resource: CisuEntity

    @classmethod
    def from_xml(cls, xml):
        distributionId = xml.getElementsByTagName("distributionID")[0].firstChild.nodeValue
        senderID = xml.getElementsByTagName("senderID")[0].firstChild.nodeValue
        dateTimeSent = xml.getElementsByTagName("dateTimeSent")[0].firstChild.nodeValue
        dateTimeExpires = xml.getElementsByTagName("dateTimeExpires")[0].firstChild.nodeValue
        distributionStatus = xml.getElementsByTagName("distributionStatus")[0].firstChild.nodeValue
        distributionKind = xml.getElementsByTagName("distributionKind")[0].firstChild.nodeValue
        resource = xml.getElementsByTagName("content")[0]

        return cls(
            distributionID=distributionId,
            senderID=senderID,
            dateTimeSent=DateType(dateTimeSent),
            dateTimeExpires=DateType(dateTimeExpires),
            distributionStatus=distributionStatus,
            distributionKind=distributionKind,
            resource=CisuEntity.from_xml(resource),
        )
