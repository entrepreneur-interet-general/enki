from flask import current_app
from dataclasses import dataclass, field, asdict
from datetime import datetime
from uuid import uuid4
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BaseEntity:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())

    def __eq__(self, other):
        return self.uuid == other.uuid