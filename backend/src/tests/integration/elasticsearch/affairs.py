import json
import os
from pathlib import Path

from typing import List

from adapters.elasticsearch.affair_repository import ElasticAffairRepository
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AlreadyExistingAffairUuid
import pytest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
from .utils import create_index

AFFAIRS_MAPPING_PATH = "../../../adapters/elasticsearch/templates/affairs.json"


def test_create_index_and_add_affairs(es_client, affairs_index_name):
    response = create_index(es_client, affairs_index_name, AFFAIRS_MAPPING_PATH)
    assert response == {'acknowledged': True, 'shards_acknowledged': True, 'index': 'affairs_test'}


def test_adding_affairs(elastic_repository: ElasticAffairRepository,
                        xml_affairs: List[AffairEntity]):
    for affair in xml_affairs:
        assert elastic_repository.add(affair=affair)
    with pytest.raises(AlreadyExistingAffairUuid):
        elastic_repository.add(affair=xml_affairs[0])


def test_index_created_and_fetch_some_affairs(elastic_repository: ElasticAffairRepository,
                                              xml_affairs: List[AffairEntity]):
    for affair in xml_affairs:
        elastic_repository.add(affair=affair)

    all_affairs: List[AffairEntity] = elastic_repository.get_all()
    assert len(all_affairs) == len(xml_affairs)


def test_location_query(elastic_repository: ElasticAffairRepository,
                        xml_affairs: List[AffairEntity]):
    for affair in xml_affairs:
        elastic_repository.add(affair=affair)
    print(len(xml_affairs))
    p = Path(__file__).resolve().parent / "../../data/polygons/chelles.json"
    with p.open() as f:
        polygon = json.load(f)

    all_affairs: List[AffairEntity] = elastic_repository.get_from_polygon(multipolygon=polygon[0][0])
    assert len(all_affairs) == len(xml_affairs)
