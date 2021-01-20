from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from domain.core.entity import Entity
from domain.phonebook.entities.methods import ContactMethods


@dataclass
@dataclass_json
class ContactEntity(Entity):
    first_name: str
    last_name: str
    contact_methods: ContactMethods
    position: str
    group_id: str
    created_at: datetime
    updated_at: datetime
