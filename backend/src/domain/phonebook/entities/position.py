from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class Company:
    name: str
    description: str


@dataclass
@dataclass_json
class Position:
    title: str
    description: str
    company: Company




