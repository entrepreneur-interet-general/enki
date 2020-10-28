from uuid import uuid4
import pytest

from ..utils.filter import filter_dict_with_keys
from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.ports.tag_repository import AlreadyExistingTagUuid, InMemoryTagRepository, NotFoundTag
from domain.tasks.services.tag_service import TagService


def initiateRepo():
    return InMemoryTagRepository()


def test_add_tag():
    repo = initiateRepo()
    uuid = str(uuid4())
    expected_title = "My title"
    TagService.add_tag(uuid=uuid, title=expected_title, repo=repo)

    print(repo.tags[0])
    assert repo.tags[0] == TagEntity(uuid=uuid, title=expected_title)


def test_fails_to_add_tag_when_already_exists():
    repo = initiateRepo()

    tag1_uuid = str(uuid4())
    serialized_tag1 = {
        "uuid": tag1_uuid,
        "title": "Tag 1 title"
    }
    tag1 = TagEntity(uuid=tag1_uuid, title=serialized_tag1["title"])
    repo.set_tags([tag1])

    with pytest.raises(AlreadyExistingTagUuid):
        TagService.add_tag(tag1_uuid, "Some title", repo=repo)


def test_list_tags():
    repo = initiateRepo()
    tag1_uuid = str(uuid4())
    serialized_tag1 = {
        "uuid": tag1_uuid,
        "title": "Tag 1 title",
    }
    tag1 = TagEntity(uuid=tag1_uuid, title=serialized_tag1["title"])
    repo.set_tags([tag1])

    tags = TagService.list_tags(repo)

    assert len(tags) == 1
    assert filter_dict_with_keys(tags[0], serialized_tag1) == serialized_tag1


def test_get_by_uuid_when_not_present():
    repo = initiateRepo()
    with pytest.raises(NotFoundTag):
        TagService.get_by_uuid("not_in_repo_uuid", repo)


def test_get_by_uuid_when_tag_present():
    repo = initiateRepo()

    tag1_uuid = str(uuid4())
    serialized_tag1 = {
        "uuid": tag1_uuid,
        "title": "Tag 1 title"
    }
    tag1 = TagEntity(uuid=tag1_uuid, title=serialized_tag1["title"])
    repo.set_tags([tag1])

    tag = TagService.get_by_uuid(tag1_uuid, repo)
    assert filter_dict_with_keys(tag, serialized_tag1) == serialized_tag1
