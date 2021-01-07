from typing import List, Union

from sqlalchemy.orm import Session

from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.ports.information_repository import AbstractInformationRepository, AlreadyExistingInformationUuid, NotFoundInformation
from domain.tasks.entities.info_entity import InformationEntity
from domain.tasks.entities.tag_entity import TagEntity
from .repository import PgRepositoryMixin


class PgInformationRepository(PgRepositoryMixin, AbstractInformationRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=InformationEntity)
        AbstractInformationRepository.__init__(self)

    def add_tag_to_information(self, information: InformationEntity, tag: TagEntity) -> None:
        information.tags.append(tag)
        self.commit()

    def remove_tag_to_information(self, information: InformationEntity, tag: TagEntity) -> None:
        information.tags.remove(tag)
        self.commit()

    def _match_uuid(self, uuid: str) -> InformationEntity:
        matches = self.session.query(InformationEntity).filter(InformationEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, information: InformationEntity) -> None:
        if self._match_uuid(information.uuid):
            raise AlreadyExistingInformationUuid()
        self.session.add(information)
        self.commit()

    def get_all(self) -> List[InformationEntity]:
        return self.session.query(self.entity_type).all()

    def _get_tag_by_information(self, uuid: str, tag_uuid: str) -> Union[TagEntity, None]:
        print(f"_get_tag_by_information uuid {uuid} and tag_uuid {tag_uuid}")
        match = self.get_by_uuid(uuid=uuid)
        matches = [tag for tag in match.tags if tag.uuid == tag_uuid]
        if not matches:
            return None
        return matches[0]
