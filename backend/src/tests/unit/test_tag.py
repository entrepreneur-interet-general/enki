import random

from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.schemas import TagSchema


def test_tag_load(tag_data):
    tag: TagEntity = TagSchema().load(tag_data)
    assert isinstance(tag, TagEntity)
    assert tag.title == tag_data["title"]
