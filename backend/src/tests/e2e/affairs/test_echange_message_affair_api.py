import pathlib

import pytest
from flask import Response
from flask.testing import FlaskClient

BASE_PATH_ECHANGES: str = "/api/v1/echanges/messages"
BASE_PATH_AFFAIRS: str = "/api/enki/v1/affairs"

filenames = list(pathlib.Path(pathlib.Path(__file__).parent.absolute()).glob("../data/*.xml"))


@pytest.mark.parametrize("filename", filenames)
def test_retrieve_random_affair(filename: pathlib.Path, client: FlaskClient):
    with open(str(filename), 'r') as f:
        post_new_affair_response = post_new_affair(client=client, xml_string=str(f.read()))
    assert post_new_affair_response.status_code == 200
    assert post_new_affair_response.json == {"message": "success"}


def test_retrieve_random_affairs(client: FlaskClient):
    get_affairs_reponse = get_affairs(client=client)
    assert get_affairs_reponse.status_code == 200
    assert len(get_affairs_reponse.json["data"]) == len(filenames)


def post_new_affair(client: FlaskClient, xml_string) -> Response:
    return client.post(BASE_PATH_ECHANGES,
                       data=xml_string,
                       headers={'Content-Type': "text/xml"})


def get_affairs(client: FlaskClient) -> Response:
    return client.get(BASE_PATH_AFFAIRS)
