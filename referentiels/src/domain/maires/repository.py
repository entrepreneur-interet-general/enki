import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException
from .entity import MaireEntity

mairesList = List[MaireEntity]


class NotFoundMaire(HTTPException):
    code = 404
    description = "Ce maire n'existe pas"


class AlreadyExistingMaireUuid(HTTPException):
    code = 409
    description = "Ce maire existe déjà"


class AbstractMaireRepository(abc.ABC):

    def add(self, maire: MaireEntity) -> None:
        if self._match_uuid(maire.uuid):
            raise AlreadyExistingMaireUuid()
        self._add(maire)

    def get_one(self) -> MaireEntity:
        return self.get_all()[0]

    def get_many(self, n: int) -> List[MaireEntity]:
        return self.get_all()[0:n]

    def get_by_uuid(self, uuid: str) -> MaireEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundMaire
        return match

    @abc.abstractmethod
    def _add(self, entity: MaireEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> mairesList:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[MaireEntity, None]:
        raise NotImplementedError


class InMemoryMaireRepository(AbstractMaireRepository):
    _maires: mairesList = []

    def _add(self, entity: MaireEntity):
        self._maires.append(entity)

    def get_all(self) -> mairesList:
        return self._maires

    def _match_uuid(self, uuid: str) -> List[MaireEntity]:
        return [maire for maire in self._maires if maire.uuid == uuid]

    # next methods are only for test purposes
    @property
    def maires(self) -> mairesList:
        return self._maires

    def set_maires(self, maires: mairesList) -> None:
        self._maires = maires
