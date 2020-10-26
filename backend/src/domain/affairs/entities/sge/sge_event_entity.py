from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from .sge_enums import SgeEventType


@dataclass_json
@dataclass
class SgeEventEntity:
    pass
    id: str
    auteur: str
    type: SgeEventType
    date: datetime
    id_contenu: str
    contenu: dict
