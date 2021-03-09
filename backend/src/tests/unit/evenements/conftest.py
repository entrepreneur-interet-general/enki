import random
from typing import Dict

import pytest

from domain.evenements.entities.evenement_entity import EvenementEntity
from domain.evenements.entities.message_entity import MessageEntity
from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.schemas import TagSchema, MessageSchema, EvenementSchema
from domain.users.entities.user import UserEntity
from domain.users.schemas.user import UserSchema


@pytest.fixture
def tag_data() -> Dict:
    return {
        "title": f"title-{random.randint(1, 100)}",
        "creator_id": f"creator-{random.randint(1, 100)}",
    }


@pytest.fixture
def tag(tag_data) -> TagEntity:
    return TagSchema().load(tag_data)


@pytest.fixture
def message_data() -> Dict:
    return {
        "title": f"title-{random.randint(1, 100)}",
        "description": f"description-{random.randint(1, 100)}",
        "evenement_id": f"evenement-{random.randint(1, 100)}",
        "type": "info",
    }


@pytest.fixture
def user_data() -> Dict:
    return {
        "first_name": "ok",
        "last_name": "oklast",
        "group_type": "prefecture",
        "group_id": "420d5a33-9b28-49a5-b878-7d89990470d8",
        "position_id": "af8571f6-a117-4ae4-9540-739b0fa5ddce"
    }


@pytest.fixture
def user(user_data) -> UserEntity:
    return UserSchema().load(user_data)


@pytest.fixture
def message(message_data) -> MessageEntity:
    return MessageSchema().load(message_data)


@pytest.fixture
def evenement_data() -> Dict:
    return {
        "description": f"description-{random.randint(1, 100)}",
        "started_at": "2012-04-23T18:25:43.511Z",
        "title": f"title-{random.randint(1, 100)}",
        "type": "natural",
        "uuid": f"uuid-{random.randint(1, 100)}",
    }


@pytest.fixture
def evenement(evenement_data) -> EvenementEntity:
    return EvenementSchema().load(evenement_data)


@pytest.fixture
def tag_factory(tag_data):
    def build_tag() -> TagEntity:
        return TagSchema().load(tag_data)

    return build_tag


@pytest.fixture
def message_factory(message_data):
    def build_message() -> MessageEntity:
        return MessageSchema().load(message_data)

    return build_message
