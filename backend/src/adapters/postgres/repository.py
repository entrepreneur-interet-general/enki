from http.client import HTTPException

from sqlalchemy.orm.session import Session
from typing import List


class NotFoundException(HTTPException):
    code = 404


class PgRepositoryMixin:
    def __init__(self, session: Session, entity_type):
        self.session = session
        self.entity_type = entity_type

    def commit(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def _match_uuid(self, uuid: str):
        matches = self.session.query(self.entity_type).filter(self.entity_type.uuid == uuid).all()
        if not matches:
            raise NotFoundException
        return matches[0]

    def _add(self, obj: any):
        self.session.add(obj)
        self.commit()

    def get_all(self) -> List[any]:
        return self.session.query(self.entity_type).all()
