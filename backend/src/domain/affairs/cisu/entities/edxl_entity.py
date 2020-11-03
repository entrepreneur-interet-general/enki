import pathlib
from uuid import uuid4

from dataclasses import dataclass

from .cisu_entity import CisuEntity
from .commons import DateType
from .commons.utils import get_data_from_tag_name


@dataclass
class EdxlEntity:
    """

    """
    distributionID: str
    senderID: str
    dateTimeSent: DateType
    dateTimeExpires: DateType
    distributionStatus: str
    distributionKind: str
    resource: CisuEntity

    @classmethod
    def from_xml(cls, xml):
        distribution_id = get_data_from_tag_name(xml, "distributionID")
        sender_id = get_data_from_tag_name(xml, "senderID")
        date_time_sent = get_data_from_tag_name(xml, "dateTimeSent")
        date_time_expires = get_data_from_tag_name(xml, "dateTimeExpires")
        distribution_status = get_data_from_tag_name(xml, "distributionStatus")
        distribution_kind = get_data_from_tag_name(xml, "distributionKind")
        resource = xml.getElementsByTagName("content")[0]

        return cls(
            distributionID=distribution_id,
            senderID=sender_id,
            dateTimeSent=DateType(date_time_sent),
            dateTimeExpires=DateType(date_time_expires),
            distributionStatus=distribution_status,
            distributionKind=distribution_kind,
            resource=CisuEntity.from_xml(resource),
        )

    def to_xml(self) -> str:
        from jinja2 import Environment, FileSystemLoader
        xml_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(), '../templates/')
        print(xml_path)
        env = Environment(loader=FileSystemLoader(str(xml_path)))
        template = env.get_template('message.xml')
        return template.render(edxl=self)
