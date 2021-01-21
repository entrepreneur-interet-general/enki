from typing import List, Union

from sqlalchemy.orm import Session

from domain.messages.entities.resource import ResourceEntity
from domain.messages.ports.resource_repository import AlreadyExistingResourceUuid, AbstractResourceRepository
from .repository import PgRepositoryMixin

resourcesList = List[ResourceEntity]


class PgResourceRepository(PgRepositoryMixin, AbstractResourceRepository):
    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=ResourceEntity)
        AbstractResourceRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[ResourceEntity, None]:
        matches = self.session.query(self.entity_type).filter(self.entity_type.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, resource: ResourceEntity):
        if self._match_uuid(resource.uuid):
            raise AlreadyExistingResourceUuid()
        self.session.add(resource)
        self.commit()

    def get_all(self) -> resourcesList:
        return self.session.query(self.entity_type).all()

    def _match_uuids(self, uuids: List[str]) -> resourcesList:
        matches = self.session.query(self.entity_type).filter(self.entity_type.uuid.in_(uuids)).all()
        return matches

    def _delete(self, resource: ResourceEntity) -> bool:
        self.session.delete(resource)
        return True