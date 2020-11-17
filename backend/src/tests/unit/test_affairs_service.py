from uuid import uuid4
import pytest
import pathlib

from domain.affairs.ports.affair_repository import AbstractAffairRepository, AlreadyExistingAffairUuid
from domain.affairs.services.affair_service import AffairService

BASE_PATH_ECHANGES: str = "/api/v1/echanges/messages"
BASE_PATH_AFFAIRS: str = "/api/enki/v1/affairs"

filenames = list(pathlib.Path(pathlib.Path(__file__).parent.absolute()).glob("../data/*.xml"))


@pytest.mark.parametrize("filename", filenames)
def test_add_affair(filename: pathlib.Path, affair_repo: AbstractAffairRepository):
    with open(str(filename), 'r') as f:
        affair_xml_string = str(f.read())
        AffairService.add_affair(xml_string=affair_xml_string, repo=affair_repo)

    affairs = AffairService.list_affairs(repo=affair_repo)
    assert isinstance(affairs, list)
    assert isinstance(affairs[0], dict)
    assert len(affairs) == 1


@pytest.mark.parametrize("filename", filenames)
def test_add_affair(filename: pathlib.Path, affair_repo: AbstractAffairRepository):
    with open(str(filename), 'r') as f:
        affair_xml_string = str(f.read())
        AffairService.add_affair(xml_string=affair_xml_string, repo=affair_repo)
        with pytest.raises(AlreadyExistingAffairUuid):
            AffairService.add_affair(xml_string=affair_xml_string, repo=affair_repo)


def test_add_multiple_affair(affair_repo: AbstractAffairRepository):
    for filename in filenames:
        with open(str(filename), 'r') as f:
            affair_xml_string = str(f.read())
            AffairService.add_affair(xml_string=affair_xml_string, repo=affair_repo)

    affairs = AffairService.list_affairs(repo=affair_repo)
    assert isinstance(affairs, list)
    assert isinstance(affairs[0], dict)
    assert len(affairs) == len(filenames)
