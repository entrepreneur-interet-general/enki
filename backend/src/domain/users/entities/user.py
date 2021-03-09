from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import List

from domain.core.entity import Entity
from domain.users.entities.contact import ContactEntity
from domain.users.entities.group import UserPositionEntity, GroupType


class ThisUserDoesNotFavoriteThisContact:
    code = 404
    description = "Cet utilisateur n'a pas mis ce contact en favoris"


@dataclass_json
@dataclass
class UserEntity(Entity):
    """

    """
    first_name: str
    last_name: str
    position_id: str = field(default_factory=lambda: None)
    group_id: str = field(default_factory=lambda: None)
    group_type: GroupType = field(default_factory=lambda: None)
    contacts: List[ContactEntity] = field(default_factory=lambda: [])
    position: UserPositionEntity = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def add_contact(self, contact: ContactEntity):
        self.contacts.append(contact)

    def remove_contact(self, contact: ContactEntity):
        self.contacts.remove(contact)

    def get_contacts(self):
        return self.contacts

    def get_contact(self, contact: ContactEntity):
        matches = [contact for contact in self.contacts if contact.uuid == contact.uuid]
        if not matches:
            raise ThisUserDoesNotFavoriteThisContact()
        return matches[0]

    def __repr__(self):
        return f"UserEntity {self.uuid} : {self.first_name}, {self.last_name}"
