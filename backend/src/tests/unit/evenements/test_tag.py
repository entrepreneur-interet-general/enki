import random

from slugify import slugify

from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.schemas.message_tag_schema import TagSchema


def test_tag_load(tag_data):
    tag: TagEntity = TagSchema().load(tag_data)
    assert isinstance(tag, TagEntity)
    assert tag.title == tag_data["title"]
    assert tag.slug == slugify(tag_data["title"])
