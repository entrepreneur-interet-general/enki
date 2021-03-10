import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from dataclasses_json import DataClassJsonMixin
from werkzeug.exceptions import HTTPException

from domain.core.entity import Entity
from domain.users.entities.user import UserEntity


class InvitationNotActiveAnymore(HTTPException):
    code = 406
    description = "Cette invitation n'est plus active"


@dataclass
class InvitationEntity(DataClassJsonMixin, Entity):
    token: str = field(init=False)
    creator_id: str
    group_id: str
    group_type: str
    invitation_url: str = field(init=False)
    creator: UserEntity = field(default_factory=lambda: None)
    user_id: Optional[str] = field(default_factory=lambda: None)
    email: Optional[str] = field(default_factory=lambda: None)
    phone_number: Optional[str] = field(default_factory=lambda: None)
    validated_at: Optional[datetime] = field(default_factory=lambda: None)
    expire_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=1))
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def __post_init__(self):
        self.token = secrets.token_urlsafe()
        self.invitation_url = f"http://localhost:1337/invitation?token={self.token}"
        print()

    @property
    def is_active(self) -> bool:
        return self.expire_at > datetime.now() and not self.validated_at

    def validate(self):
        if not self.is_active:
            raise InvitationNotActiveAnymore

    def close_invitation(self, user_id: str = None):
        self.user_id = user_id
        self.validated_at = datetime.now()
