import glob
from typing import List
import xml.dom.minidom
import logging

from cisu.entities.edxl_entity import EdxlEntity

from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository, affairsList
import pathlib


class XmlCisuRepository(AbstractAffairRepository):

    def __init__(self, xml_path: str = 'data/'):

        self.xml_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(), xml_path)
        logging.info(f"self.xml_path {self.xml_path}")
        self.all_affairs: List[AffairEntity] = []
        self._list_xml_files()

    def _add(self, entity: AffairEntity):
        self.all_affairs.append(entity)

    def get_all(self) -> affairsList:
        logging.info(f"self.all_affairs {self.all_affairs}")
        return self.all_affairs

    def _match_uuid(self, uuid: str) -> AffairEntity:
        _matches = [affair for affair in self.all_affairs if affair.distributionID == uuid]
        if _matches:
            return _matches[0]

    def _list_xml_files(self):
        for xml_file in self.xml_path.glob("*.xml"):
            logging.info(f"self.all_affairs {self.all_affairs}")
            self._add(self.build_affair_from_xml_file(str(xml_file)))

    @staticmethod
    def build_affair_from_xml_string(xml_string: str) -> AffairEntity:
        affair_dom = xml.dom.minidom.parseString(xml_string)
        edxl_message = EdxlEntity.from_xml(affair_dom)
        return AffairEntity(**edxl_message.resource.message.choice.to_dict())

    @staticmethod
    def build_affair_from_xml_file(xml_path: str) -> AffairEntity:
        affair_dom = xml.dom.minidom.parse(xml_path)
        edxl_message = EdxlEntity.from_xml(affair_dom)
        return AffairEntity(**edxl_message.resource.message.choice.to_dict())

    def _get_from_polygon(self, multipolygon: List):
        return self.all_affairs