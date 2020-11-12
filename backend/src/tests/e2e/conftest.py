import pytest
from dotenv import load_dotenv
from entrypoints.flask_app import create_app


@pytest.fixture(scope="session")
def app():
    load_dotenv(".envs/.test/.env.flaskenv")
    app = create_app(testing=True)
    yield app
    app.context.reset()


@pytest.fixture(scope="session")
def client(app):
    with app.test_client() as client:
        yield client

