from domain.messages.entities.tag_entity import TagEntity
from domain.messages.schemas.schema import TagSchema
import random


def build_tag_data():
    return {
        "title": f"title-{random.randint(1, 100)}",
        "creator_id": f"creator-{random.randint(1, 100)}",
    }


def test_tag_load():
    tag_data = build_tag_data()
    tag: TagEntity = TagSchema().load(tag_data)
    assert isinstance(tag, TagEntity)
    assert tag.title == tag_data["title"]
