import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException

from domain.phonebook.entities.company import CompanyEntity

CompanysList = List[CompanyEntity]


class AlreadyExistingCompanyUuid(HTTPException):
    code = 409
    description = "Company already exists"


class NotFoundCompany(HTTPException):
    code = 404
    description = "Company not found"


class AbstractCompanyRepository(abc.ABC):
    def add(self, company: CompanyEntity) -> None:
        if self._match_uuid(company.uuid):
            raise AlreadyExistingCompanyUuid()
        self._add(company)
        # TODO : test if title already exists

    def get_by_uuid(self, uuid: str) -> CompanyEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundCompany
        return matches

    def get_by_uuid_list(self, uuids: List[str]) -> List[CompanyEntity]:
        matches = self._match_uuids(uuids)
        if not matches:
            raise NotFoundCompany
        return matches

    @abc.abstractmethod
    def get_all(self) -> CompanysList:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, company: CompanyEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[CompanyEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuids(self, uuids: List[str]) -> List[CompanyEntity]:
        raise NotImplementedError
