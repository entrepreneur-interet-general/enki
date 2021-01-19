from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class ContactMethods:
    tel: str
    email: str
    address: str


@dataclass
@dataclass_json
class ContactEntity:
    first_name: str
    last_name: str
    contact_methods: ContactMethods



