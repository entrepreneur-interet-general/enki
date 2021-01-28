import json
from uuid import uuid4
import pytest
import pathlib

import requests_mock
from domain.affairs.ports.affair_repository import AbstractAffairRepository, AlreadyExistingAffairUuid
from domain.affairs.services.affair_service import AffairService

BASE_PATH_ECHANGES: str = "/api/v1/echanges/messages"
BASE_PATH_AFFAIRS: str = "/api/enki/v1/affairs"

filenames = list(pathlib.Path(pathlib.Path(__file__).parent.absolute()).glob("../../data/*.xml"))
response_folder = pathlib.Path(pathlib.Path(__file__).parent.absolute()) / "../../data/response/sig"


@pytest.mark.parametrize("filename", filenames)
@pytest.mark.skip(reason="no way of currently testing this")
def test_add_affair(filename: pathlib.Path, affair_repo: AbstractAffairRepository):
    with open(str(filename), 'r') as f:
        affair_xml_string = str(f.read())
        AffairService.add_affair_from_xml(xml_string=affair_xml_string, uow=affair_repo)

    affairs = AffairService.list_affairs(repo=affair_repo)
    assert isinstance(affairs, list)
    assert isinstance(affairs[0], dict)
    assert len(affairs) == 1

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.parametrize("filename", filenames)
def test_add_affair(filename: pathlib.Path, affair_repo: AbstractAffairRepository):
    with open(str(filename), 'r') as f:
        affair_xml_string = str(f.read())
        AffairService.add_affair_from_xml(xml_string=affair_xml_string, uow=affair_repo)
        with pytest.raises(AlreadyExistingAffairUuid):
            AffairService.add_affair_from_xml(xml_string=affair_xml_string, uow=affair_repo)

@pytest.mark.skip(reason="no way of currently testing this")
def test_add_multiple_affair(affair_repo: AbstractAffairRepository):
    for filename in filenames:
        with open(str(filename), 'r') as f:
            affair_xml_string = str(f.read())
            AffairService.add_affair_from_xml(xml_string=affair_xml_string, uow=affair_repo)

    affairs = AffairService.list_affairs(repo=affair_repo)
    assert isinstance(affairs, list)
    assert isinstance(affairs[0], dict)
    assert len(affairs) == len(filenames)

@pytest.mark.skip(reason="no way of currently testing this")
def test_affairs_service_with_unknow_code(affair_repo: AbstractAffairRepository):
    for filename in filenames:
        with open(str(filename), 'r') as f:
            affair_xml_string = str(f.read())
            AffairService.add_affair_from_xml(xml_string=affair_xml_string, uow=affair_repo)

    with (response_folder / "empty.json").open() as f:
        empty_response = json.load(f)

    with requests_mock.Mocker(real_http=True) as m:
        m.register_uri('GET', 'http://localhost:8083/decoupage-administratif/territoire/codes?codesInsee=99999',
                       json=empty_response)

        affairs = AffairService.list_affairs_by_insee_and_postal_codes(insee_code="99999",
                                                                       postal_code=None,
                                                                       repo=affair_repo)
    assert isinstance(affairs, list)
    assert affairs == []

@pytest.mark.skip(reason="no way of currently testing this")
def test_affairs_service_with_know_code_chelles(affair_repo: AbstractAffairRepository):
    for filename in filenames:
        with open(str(filename), 'r') as f:
            affair_xml_string = str(f.read())
            AffairService.add_affair_from_xml(xml_string=affair_xml_string, uow=affair_repo)

    with (response_folder / "chelles.json").open() as f:
        chelles_response = json.load(f)

    with requests_mock.Mocker(real_http=True) as m:
        m.register_uri('GET', 'http://localhost:8083/decoupage-administratif/territoire/codes?codesInsee=77108',
                       json=chelles_response)

        affairs = AffairService.list_affairs_by_insee_and_postal_codes(insee_code="77108",
                                                                       postal_code=None,
                                                                       repo=affair_repo)
    assert isinstance(affairs, list)
    assert len(affairs) == 4
