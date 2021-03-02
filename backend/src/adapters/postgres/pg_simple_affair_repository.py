from typing import List, Union

from flask import current_app
from geoalchemy2 import WKBElement
from sqlalchemy.orm import Session

from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository, AlreadyExistingAffairUuid
from domain.affairs.ports.simple_affair_repository import AbstractSimpleAffairRepository
from domain.evenements.entity import EvenementEntity
from .repository import PgRepositoryMixin


class PgSimpleAffairRepository(PgRepositoryMixin, AbstractSimpleAffairRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=SimpleAffairEntity)
        AbstractAffairRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[SimpleAffairEntity, None]:
        matches = self.session.query(SimpleAffairEntity).filter(SimpleAffairEntity.uuid == uuid).all()
        if matches:
            return matches[0]
        return None

    def _match_by_affair_uuid(self, uuid: str) -> Union[SimpleAffairEntity, None]:
        matches = self.session.query(SimpleAffairEntity).filter(SimpleAffairEntity.sge_hub_id == uuid).all()
        if matches:
            return matches[0]
        return None

    def _add(self, affair: SimpleAffairEntity) -> None:
        if self._match_uuid(affair.uuid):
            raise AlreadyExistingAffairUuid()
        self.session.add(affair)

    def get_all(self) -> List[SimpleAffairEntity]:
        return self.session.query(SimpleAffairEntity).all()

    def assign_evenement_to_affair(self, affair: SimpleAffairEntity, evenement: EvenementEntity) -> SimpleAffairEntity:
        affair.evenement = evenement
        return affair

    def delete_affair_from_evenement(self, affair: SimpleAffairEntity) -> SimpleAffairEntity:
        affair.evenement_id = None
        return affair

    def get_by_evenement(self, uuid: str) -> List[SimpleAffairEntity]:
        matches = self.session.query(SimpleAffairEntity).filter(SimpleAffairEntity.evenement_id == uuid).all()
        return matches

    def _match_uuids(self, uuids: List[str]):
        matches = self.session.query(self.entity_type).filter(self.entity_type.uuid.in_(uuids)).all()
        return matches

    def match_polygons(self, polygon: Union[List, str]) -> List[SimpleAffairEntity]:
        current_app.logger.info(f"Polygon {polygon}")
        current_app.logger.info(f"Type(Polygon) {type(polygon)}")
        if isinstance(polygon, list):
            polygon_query_string = f"POLYGON(({' ,'.join([' '.join([str(e[1]), str(e[0])]) for e in polygon])}))"
        elif isinstance(polygon, WKBElement):
            polygon_query_string = polygon
        else:
            polygon_query_string = polygon

        matches = self.session.query(self.entity_type).filter(
            self.entity_type.location.ST_Within(polygon_query_string)
        ).all()

        return matches
