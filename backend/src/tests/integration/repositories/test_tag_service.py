from uuid import uuid4

import pytest

from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.ports.tag_repository import AlreadyExistingTagUuid, NotFoundTag, \
    AbstractTagRepository


def test_add_tag(tag_repo: AbstractTagRepository):
    uuid = str(uuid4())
    expected_title = "My title"
    tag = TagEntity(uuid=uuid, title=expected_title,)
    tag_repo.add(tag)

    assert tag_repo.get_all()[0] == tag


def test_fails_to_add_tag_when_already_exists(tag_repo: AbstractTagRepository):

    tag1_uuid = str(uuid4())
    serialized_tag1 = {
        "uuid": tag1_uuid,
        "title": "Tag 1 title"
    }
    tag1 = TagEntity(uuid=tag1_uuid, title=serialized_tag1["title"])
    tag_repo.add(tag1)

    with pytest.raises(AlreadyExistingTagUuid):
        tag_repo.add(tag1)


def test_list_tags(tag_repo: AbstractTagRepository):
    tag1_uuid = str(uuid4())
    serialized_tag1 = {
        "uuid": tag1_uuid,
        "title": "Tag 1 title",
    }
    tag1 = TagEntity(uuid=tag1_uuid, title=serialized_tag1["title"])
    tag_repo.add(tag1)

    tags = tag_repo.get_all()

    assert len(tags) == 1
    assert tags[0] == tag1


def test_get_by_uuid_when_not_present(tag_repo: AbstractTagRepository):
    with pytest.raises(NotFoundTag):
        tag_repo.get_by_uuid("not_in_repo_uuid")


def test_get_by_uuid_when_tag_present(tag_repo: AbstractTagRepository):
    tag1_uuid = str(uuid4())
    serialized_tag1 = {
        "uuid": tag1_uuid,
        "title": "Tag 1 title"
    }
    tag1 = TagEntity(uuid=tag1_uuid, title=serialized_tag1["title"])
    tag_repo.add(tag1)

    tag = tag_repo.get_by_uuid(tag1_uuid)
    assert tag == tag1
