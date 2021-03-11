from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Union, List, Optional

from dataclasses_json import dataclass_json
from domain.core.entity import Entity
from domain.evenements.entities.evenement_entity import EvenementEntity
from domain.users.entities.user import UserEntity


@dataclass_json
@dataclass
class MeetingEntity(Entity):
    evenement_id: str
    evenement: EvenementEntity
    link: str = field(init=False)
    creator_id: Optional[str] = field(default_factory=lambda: None)
    creator: UserEntity = field(default_factory=lambda: None)
    participants: List[UserEntity] = field(default_factory=lambda: [])
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
    closed_at: datetime = field(default_factory=lambda: None)

    def __post_init__(self):
        self.link = f"https://meet.jit.si/{self.evenement.title}"

    def __eq__(self, other):
        return self.uuid == other.uuid

    def set_creator(self, user: UserEntity):
        self.creator_id = user.uuid

    def add_participant(self, user: UserEntity):
        self.participants.append(user)
