from dataclasses import dataclass
from dataclasses_json import dataclass_json

from domain.phonebook.entities.position import Position


@dataclass
@dataclass_json
class ContactMethods:
    tel: str
    email: str
    address: str
    position: Position


@dataclass
@dataclass_json
class ContactEntity:
    first_name: str
    last_name: str
    contact_methods: ContactMethods



