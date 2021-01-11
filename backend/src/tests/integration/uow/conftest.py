import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from entrypoints.config import EnkiConfig
from service_layer.unit_of_work import SqlAlchemyUnitOfWork, InMemoryUnitOfWork, AbstractUnitOfWork


@pytest.fixture(scope="session")
def config() -> Engine:
    load_dotenv(".envs/.test/.env.flaskenv")
    config = EnkiConfig()
    return config


@pytest.fixture(scope="function", params=["in_memory", "sqlite"])  # , "sqlite"
def uow(request, config: EnkiConfig) -> AbstractUnitOfWork:
    if request.param == "sqlite":
        uow = SqlAlchemyUnitOfWork(config=config)
    else:  # request.param == "in_memory"
        uow = InMemoryUnitOfWork(config=config)
    return uow
