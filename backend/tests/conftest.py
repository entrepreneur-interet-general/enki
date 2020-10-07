import pytest
from pathlib import Path
import time

import requests
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from adapters.postgres.orm import metadata, start_mappers
from tenacity import retry, stop_after_delay

# Could put following in config file, see in cosmic python : get_api_url, config.get_postgres_uri
test_pg_uri = 'postgresql://postgres:pg-password@localhost:5431/sapeurs-test'
test_api_url = "http://localhost:5000"

# @retry(stop=stop_after_delay(10))
# def wait_for_postgres_to_come_up(engine: Engine):
#     return engine.connect()

@pytest.fixture(scope='session')
def postgres_db():
    engine = create_engine(test_pg_uri, isolation_level='SERIALIZABLE')
    # wait_for_postgres_to_come_up(engine)
    engine.connect()
    metadata.create_all(engine)
    return engine


@retry(stop=stop_after_delay(10))
def wait_for_webapp_to_come_up():
    return requests.get(test_api_url)

# @retry(stop=stop_after_delay(10))
# def wait_for_webapp_to_come_up():
#     deadline = time.time() + 10
#     while time.time() < deadline:
#         try:
#             return requests.get(test_api_url)
#         except ConnectionError:
#             time.sleep(0.5)
#     pytest.fail('API never came up')


@pytest.fixture
def restart_api():
    (Path(__file__).parent / '../src/entrypoints/flask_app.py').touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()