from dataclasses import dataclass
from dataclasses_json import dataclass_json

from domain.phonebook.entities.contact import ContactMethods


@dataclass
@dataclass_json
class CompanyEntity(Entity):
    name: str
    description: str
    contact_methods: ContactMethods