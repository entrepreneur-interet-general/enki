import random
from typing import Dict

import pytest

from domain.users.entities.contact import ContactEntity
from domain.users.entities.user import UserEntity
from domain.users.schemas.contact import ContactSchema
from domain.users.schemas.user import UserSchema


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
def contact_data() -> Dict:
    return {
        "first_name": "ok",
        "last_name": "oklast",
        "tel": {
            "mobile": "0615409041"
        },
        "email": "r.courivaud@gmail.com",
        "address": "94 va",
        "group_type": "prefecture",
        "position_id": "165461414641",
        "group_id": "165461414641"
    }


@pytest.fixture
def contact(contact_data) -> UserEntity:
    return ContactSchema().load(contact_data)


@pytest.fixture
def contact_factory(contact_data):
    def build_contact() -> ContactEntity:
        return ContactSchema().load(contact_data)

    return build_contact
