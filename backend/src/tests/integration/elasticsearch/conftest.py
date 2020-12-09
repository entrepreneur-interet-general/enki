import pathlib
import time

import pytest
from elasticsearch import Elasticsearch
from typing import List

from adapters.elasticsearch.affair_repository import ElasticAffairRepository
from adapters.xml.xml_cisu_repository import XmlCisuRepository
from domain.affairs.entities.affair_entity import AffairEntity


@pytest.fixture(scope="session")
def es_client():
    client = Elasticsearch("localhost:9201")
    yield client


@pytest.fixture(scope="session", autouse=True)
def run_before_and_after_tests(elastic_repository, affairs_index_name, xml_affairs):
    """Fixture to execute asserts before and after a test is run"""
    elastic_repository.client.indices.delete(index=elastic_repository.index_name)
    elastic_repository.create_indice()

    for affair in xml_affairs:
        elastic_repository.add(affair=affair)
    assert True
    elastic_repository.client.indices.refresh()
    yield
    assert True
    elastic_repository.client.indices.delete(index=elastic_repository.index_name)


@pytest.fixture(scope="session")
def affairs_index_name():
    return "affairs_test"


@pytest.fixture(scope="session")
def elastic_repository(es_client, affairs_index_name) -> ElasticAffairRepository:
    repo = ElasticAffairRepository(es_client, index_name=affairs_index_name)
    return repo


@pytest.fixture(scope="session")
def xml_affairs() -> List[AffairEntity]:
    filenames = list(pathlib.Path(pathlib.Path(__file__).parent.absolute()).glob("../../data/*.xml"))
    xml_repo = XmlCisuRepository()
    affairs = [xml_repo.build_affair_from_xml_file(str(file)) for file in filenames]
    return affairs
