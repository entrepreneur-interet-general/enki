import pathlib
import pytest
from elasticsearch import Elasticsearch
from typing import List

from adapters.elasticsearch.affair_repository import ElasticAffairRepository
from adapters.xml.xml_cisu_repository import XmlCisuRepository
from domain.affairs.entities.affair_entity import AffairEntity


@pytest.fixture(scope="function")
def es_client():
    client = Elasticsearch("localhost:9201")
    try:
        yield client
    finally:
        client.indices.delete(index="*")


@pytest.fixture(scope="function")
def affairs_index_name():
    return "affairs_test"


@pytest.fixture(scope="function")
def elastic_repository(es_client, affairs_index_name) -> ElasticAffairRepository:
    repo = ElasticAffairRepository(es_client, index_name=affairs_index_name)
    yield repo


@pytest.fixture(scope="module")
def xml_affairs() -> List[AffairEntity]:
    filenames = list(pathlib.Path(pathlib.Path(__file__).parent.absolute()).glob("../../data/*.xml"))
    xml_repo = XmlCisuRepository()
    affairs = [xml_repo.build_affair_from_xml_file(str(file)) for file in filenames]
    return affairs
