import pytest

from domain.tasks.ports.tag_repository import AbstractTagRepository, InMemoryTagRepository
from domain.tasks.ports.task_repository import InMemoryTaskRepository, AbstractTaskRepository



@pytest.fixture(scope="function")
def tag_repo() -> AbstractTagRepository:
    return InMemoryTagRepository()

@pytest.fixture(scope="function")
def task_repo(tag_repo:AbstractTagRepository) -> AbstractTaskRepository:
    repo = InMemoryTaskRepository(tag_repo=tag_repo)
    repo._tasks = []
    return repo

