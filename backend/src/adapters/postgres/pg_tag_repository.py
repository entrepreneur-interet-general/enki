from typing import List

from sqlalchemy.orm import Session

from domain.tasks.ports.tag_repository import AbstractTagRepository, NotFoundTag, AlreadyExistingTagUuid
from domain.tasks.entities.tag_entity import TagEntity
from .repository import PgRepositoryMixin, NotFoundException


class PgTagRepository(PgRepositoryMixin, AbstractTagRepository):
    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=TagEntity)
        AbstractTagRepository.__init__(self)

    def _match_uuid(self, uuid: str):
        matches = self.session.query(TagEntity).filter(TagEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, tag: TagEntity):
        if self._match_uuid(tag.uuid):
            raise AlreadyExistingTagUuid()
        self.session.add(tag)
        self.commit()

    def get_all(self) -> List[TagEntity]:
        return self.session.query(self.entity_type).all()
