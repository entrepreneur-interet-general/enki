import json

from flask.testing import FlaskClient


def test_hello_enki_returns_200_and_expected_message(client: FlaskClient):
    response = client.get('/')
    body = json.loads(response.data)
    print("response data : ", json.loads(response.data))
    assert response.status_code == 200
    assert body['message'] == "Hello, Enki!"


def test_hello_enki_returns_200_and_expected_message(client: FlaskClient):
    response = client.get('/api/enki/')
    body = json.loads(response.data)
    print("response data : ", json.loads(response.data))
    assert response.status_code == 200
    assert body['message'] == "Hello, Enki!"


def test_hello_enki_returns_404(client: FlaskClient):
    response = client.get('/api/enki/v1')
    assert response.status_code == 404
