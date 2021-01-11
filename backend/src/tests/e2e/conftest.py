from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.exc import OperationalError

from adapters.postgres.orm import start_mappers, metadata
from entrypoints.config import EnkiConfig
from entrypoints.flask_app import create_app
import time


@pytest.fixture(scope="function")
def app():
    load_dotenv(".envs/.test/.env.flaskenv")
    app = create_app(testing=True)
    yield app


@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        yield client
