from datetime import datetime
from uuid import uuid4
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from .sge_enums import SgeEventType


@dataclass_json
@dataclass
class SgeEventEntity:
    pass
    id: uuid4
    auteur: str
    type: SgeEventType
    date: datetime
    id_contenu: uuid4
    contenu: dict
