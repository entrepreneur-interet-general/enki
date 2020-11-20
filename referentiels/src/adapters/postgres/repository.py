import abc
from http.client import HTTPException

from sqlalchemy.orm.session import Session
from typing import List, Any


class NotFoundException(HTTPException):
    code = 404


class PgRepositoryMixin(abc.ABC):
    def __init__(self, session: Session, entity_type: Any):
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

    def _add(self, obj: Any):
        self.session.add(obj)
        self.commit()