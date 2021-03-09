from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

from typing import Union, Optional, List

from werkzeug.exceptions import HTTPException

from domain.core.entity import Entity
from flask import current_app
from enum import Enum

from domain.core.entity import Entity
from domain.users.entities.user import UserEntity


class EvenementClosedException(HTTPException):
    code = 410
    description = "Evenement is closed"
class UserAlreadyAccessEvenement(HTTPException):
    code = 409
    description = "Cet utilisateur à déjà accès à cet évenement"


class UserHasNoAccessEvenement(HTTPException):
    code = 409
    description = "Cet utilisateur n'à pas accès à cet évenement"

class EvenementType(str, Enum):
    NATURAL = "natural"
    RASSEMBLEMENT = "rassemblement"


class EvenementRoleType(str, Enum):
    ADMIN = "admin"
    EDIT = "edit"
    VIEW = "view"


@dataclass_json
@dataclass
class UserEvenementRole(Entity):
    user_id: str
    evenement_id: str
    type: EvenementRoleType
    user: UserEntity = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    revoked_at: Optional[datetime] = field(default_factory=lambda: None)
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def is_active(self):
        return self.revoked_at > datetime.now()

    def revoke(self):
        self.revoked_at = datetime.now()


@dataclass_json
@dataclass
class EvenementEntity(Entity):
    """

    """
    title: str
    description: Union[str, None]
    type: EvenementType
    started_at: datetime
    creator_id: Optional[str] = field(default_factory=lambda: None)
    creator: Optional[UserEntity] = field(default_factory=lambda: None)
    user_roles: List[UserEvenementRole] = field(default_factory=lambda: [])
    ended_at: Union[datetime, None] = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    @property
    def closed(self):
        return self.ended_at and self.ended_at < datetime.now()

    def close(self):
        self.ended_at = datetime.now()

    def check_can_assign(self):
        if self.closed:
            raise EvenementClosedException

    def change_access_type(self, user_id: str, role_type: EvenementRoleType):
        for role in self.user_roles:
            if role.user_id == user_id:
                role.type = role_type
                return
        raise UserHasNoAccessEvenement()

    def add_user_role(self, user_role: UserEvenementRole):
        for role in self.user_roles:
            if role.user_id == user_role.user_id and user_role.uuid != role.uuid:
                raise UserAlreadyAccessEvenement()
        self.user_roles.append(user_role)

    def revoke_user_access(self, user_id):
        for user_role in self.user_roles:
            if user_role.user_id == user_id:
                self.user_role.revoke()
                return
        raise UserHasNoAccessEvenement()

    def user_has_access(self, user_id: str, role_type: EvenementRoleType = EvenementRoleType.VIEW) -> bool:
        for user_role in self.user_roles:
            if user_role.user_id == user_id and user_role.type == role_type:
                return True
        return False
