from datetime import datetime
from dataclasses import dataclass, field
import secrets
from domain.core.entity import Entity
from dataclasses_json import DataClassJsonMixin

from domain.users.entities.user import UserEntity


@dataclass
class InvitationEntity(DataClassJsonMixin, Entity):
    token: str = field(init=False)
    creator_id: str
    evenement_id: str
    creator: UserEntity
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def __post_init__(self):
        self.token = secrets.token_urlsafe()
