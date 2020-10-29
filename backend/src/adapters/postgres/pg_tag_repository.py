from typing import List

from sqlalchemy.orm import Session

from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.entities.tag_entity import TagEntity
from .repository import PgRepositoryMixin, NotFoundException


class PgTagRepository(AbstractTagRepository, PgRepositoryMixin):
    def __init__(self, session: Session):
        super().__init__(session=session, entity_type=TagEntity)
