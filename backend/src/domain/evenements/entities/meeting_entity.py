import secrets

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Union, List, Optional

from dataclasses_json import dataclass_json
from slugify import slugify

from domain.core.entity import Entity
from domain.evenements.entities.evenement_entity import EvenementEntity
from domain.users.entities.user import UserEntity


@dataclass_json
@dataclass
class MeetingEntity(Entity):
    evenement_id: str
    creator_id: str
    link: str = field(init=False)
    evenement: EvenementEntity = field(default_factory=lambda: None)
    creator: UserEntity = field(default_factory=lambda: None)
    participants: List[UserEntity] = field(default_factory=lambda: [])
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
    closed_at: datetime = field(default_factory=lambda: None)

    def __post_init__(self):
        self.build_link()

    def __eq__(self, other):
        return self.uuid == other.uuid

    def set_creator(self, creator: UserEntity):
        self.creator = creator
        self.creator_id = creator.uuid

    def set_evenement(self, evenement: EvenementEntity):
        self.evenement_id = evenement.uuid
        self.build_link()

    def build_link(self):
        self.link = f"https://meet.jit.si/{slugify(secrets.token_urlsafe())}"

    def add_participant(self, user: UserEntity):
        self.participants.append(user)
