from dataclasses import dataclass
from typing import List, Dict

from dataclasses_json import dataclass_json

from domain.phonebook.entities.company import CompanyEntity


@dataclass
@dataclass_json
class ContactMethods:
    tel: Dict[str, str]
    email: str  # Enki Profile
    address: str
    position: str
    company: CompanyEntity
