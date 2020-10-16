from typing import List

from sqlalchemy.orm import Session

from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.entities.tag_entity import TagEntity
from .repository import PgRepositoryMixin, NotFoundException


class PgTagRepository(AbstractTagRepository, PgRepositoryMixin):

    def __init__(self, session: Session):
        super().__init__(session=session, entity_type=TagEntity)

    def get_all(self) -> List[TagEntity]:
        return self.session.query(TagEntity).all()

    def _add(self, tag: TagEntity):
        self.session.add(tag)
        self.session.commit()

    def _match_uuid(self, uuid: str):
        matches = self.session.query(TagEntity).filter(TagEntity.uuid == uuid).all()
        if not matches:
            raise NotFoundException
        return matches[0]
