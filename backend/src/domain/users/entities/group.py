from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum

from typing import Union, Optional, List

from domain.core.entity import Entity


class GroupType(str, Enum):
    MAIRIE = "mairie"
    PREFECTURE = "prefecture"
    PARTENAIRE = "partenaire"
    SDIS = "SDIS"
    COZ = "COZ"
    COGIC = "COGIC"


class LocationType(str, Enum):
    VILLE = "ville"
    DEPARTEMENT = "departement"
    REGION = "region"
    ZONE = "zone"
    OTHER = "other" 


@dataclass_json
@dataclass
class LocationEntity(Entity):
    name: str
    external_id: str
    type: LocationType
    polygon: Optional[str] = None  # TODO:  Handle this


@dataclass_json
@dataclass
class GroupEntity(Entity):
    name: str
    type: GroupType
    location_id: Optional[str] = None
    location: LocationEntity = None
