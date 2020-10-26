from typing import List

from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session
from domain.affairs.entities.sge.sge_message_entity import SgeMessageEntity
from domain.affairs.ports.message_repository import AbstractSgeMessageRepository


class PgSgeMessageRepository(AbstractSgeMessageRepository):

    def __init__(self, session: Session):
        self.session = session

    def _report_message_query(self) -> Query:
        return self.session.query(SgeMessageEntity)#.filter(SgeMessageEntity.type == "Report")

    def get_all(self) -> List[SgeMessageEntity]:
        return self._report_message_query().all()

    def _match_uuid(self, uuid: str):
        return self._report_message_query().filter(SgeMessageEntity.id == uuid).all()
