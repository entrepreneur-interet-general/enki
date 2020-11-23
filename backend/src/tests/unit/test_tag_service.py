from uuid import uuid4
import pytest

from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.ports.tag_repository import AlreadyExistingTagUuid, InMemoryTagRepository, NotFoundTag, \
    AbstractTagRepository
from domain.tasks.services.tag_service import TagService
from ..helpers.filter import filter_dict_with_keys


def test_add_tag(tag_repo: AbstractTagRepository):
    uuid = str(uuid4())
    expected_title = "My title"
    TagService.add_tag(uuid=uuid, title=expected_title, repo=tag_repo)

    assert tag_repo.get_all()[0] == TagEntity(uuid=uuid, title=expected_title)


def test_fails_to_add_tag_when_already_exists(tag_repo: AbstractTagRepository):

    tag1_uuid = str(uuid4())
    serialized_tag1 = {
        "uuid": tag1_uuid,
        "title": "Tag 1 title"
    }
    tag1 = TagEntity(uuid=tag1_uuid, title=serialized_tag1["title"])
    tag_repo.add(tag1)

    with pytest.raises(AlreadyExistingTagUuid):
        TagService.add_tag(tag1_uuid, "Some title", repo=tag_repo)


def test_list_tags(tag_repo: AbstractTagRepository):
    tag1_uuid = str(uuid4())
    serialized_tag1 = {
        "uuid": tag1_uuid,
        "title": "Tag 1 title",
    }
    tag1 = TagEntity(uuid=tag1_uuid, title=serialized_tag1["title"])
    tag_repo.add(tag1)

    tags = TagService.list_tags(tag_repo)

    assert len(tags) == 1
    assert filter_dict_with_keys(tags[0], serialized_tag1) == serialized_tag1


def test_get_by_uuid_when_not_present(tag_repo: AbstractTagRepository):
    with pytest.raises(NotFoundTag):
        TagService.get_by_uuid("not_in_repo_uuid", tag_repo)


def test_get_by_uuid_when_tag_present(tag_repo: AbstractTagRepository):
    tag1_uuid = str(uuid4())
    serialized_tag1 = {
        "uuid": tag1_uuid,
        "title": "Tag 1 title"
    }
    tag1 = TagEntity(uuid=tag1_uuid, title=serialized_tag1["title"])
    tag_repo.add(tag1)

    tag = TagService.get_by_uuid(tag1_uuid, tag_repo)
    assert filter_dict_with_keys(tag, serialized_tag1) == serialized_tag1
