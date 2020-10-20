import glob
from typing import List
import xml.dom.minidom
import logging
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository, affairsList
import pathlib


class XmlCisuRepository(AbstractAffairRepository):

    def __init__(self, xml_path: str = 'data/'):

        self.xml_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(),xml_path)
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
            dom = xml.dom.minidom.parse(str(xml_file))
            self._add(AffairEntity.from_xml(dom))

