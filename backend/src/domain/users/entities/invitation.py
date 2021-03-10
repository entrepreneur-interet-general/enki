import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from dataclasses_json import DataClassJsonMixin

from domain.core.entity import Entity
from domain.users.entities.user import UserEntity


@dataclass
class InvitationEntity(DataClassJsonMixin, Entity):
    token: str = field(init=False)
    creator_id: str
    invitation_url: str = field(init=False)
    creator: UserEntity = field(default_factory=lambda: None)
    user_id: Optional[str] = field(default_factory=lambda: None)
    email: Optional[str] = field(default_factory=lambda: None)
    validated_at: Optional[datetime] = field(default_factory=lambda: None)
    expire_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=1))
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def __post_init__(self):
        self.token = secrets.token_urlsafe()
        self.invitation_url = f"http://localhost:1337/signup?token={self.token}"

    def is_active(self):
        return self.expire_at < datetime.now() and not self.validated_at

    def validate(self, email: str, user_id: str = None):
        self.email = email
        self.user_id = user_id
        self.validated_at = datetime.now()
