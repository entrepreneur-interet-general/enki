from typing import List, Union

from sqlalchemy.orm import Session

from ...domain.elus.maires.repository import mairesList
from ...domain.elus.maires.entity import MaireEntity
from ...domain.elus.maires.repository import AbstractMaireRepository, AlreadyExistingMaireUuid
from .repository import PgRepositoryMixin


class PgMaireRepository(PgRepositoryMixin, AbstractMaireRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=MaireEntity)
        AbstractMaireRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[MaireEntity, None]:
        matches = self.session.query(self.entity_type).filter(self.entity_type.id == uuid).all()
        if matches:
            return matches[0]

    def _add(self, maire: MaireEntity):
        if self._match_uuid(maire.id):
            raise AlreadyExistingMaireUuid()
        self.session.add(maire)
        self.commit()

    def get_by_dept_code(self, dept_code, from_: int, to_: int) -> mairesList:
        matches = self.session.query(self.entity_type).filter(
            self.entity_type.dept_code == dept_code
        ).limit(to_).offset(from_)
        return matches

    def get_by_city_code(self, city_code, from_: int, to_: int) -> mairesList:
        matches = self.session.query(self.entity_type).filter(self.entity_type.id == city_code).all()
        return matches

    def get_all(self, from_: int, to_: int) -> List[MaireEntity]:
        return self.session.query(self.entity_type).limit(to_).offset(from_)
