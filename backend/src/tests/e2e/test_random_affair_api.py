from typing import Dict
from uuid import uuid4

import pathlib
from flask import Response
from flask.testing import FlaskClient

BASE_PATH_RANDOM_AFFAIRS: str = "/api/enki/v1/affairs/random"
BASE_PATH_RANDOM_AFFAIR: str = "/api/enki/v1/affair/random"


def test_retrieve_random_affair(app, client: FlaskClient):
    get_random_affair_response: Response = get_random_affair(client)
    assert get_random_affair_response.status_code == 200
    assert isinstance(get_random_affair_response.json["affair"], dict)


def test_retrieve_random_affairs(app, client: FlaskClient):
    get_random_affair_response: Response = get_random_affairs(client)
    assert get_random_affair_response.status_code == 200
    assert len(get_random_affair_response.json["affairs"]) == 10


def get_random_affair(client: FlaskClient) -> Response:
    return client.get(BASE_PATH_RANDOM_AFFAIR)


def get_random_affairs(client: FlaskClient) -> Response:
    return client.get(BASE_PATH_RANDOM_AFFAIRS)
