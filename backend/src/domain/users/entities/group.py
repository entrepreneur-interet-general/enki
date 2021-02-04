from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum

from slugify import slugify
from typing import Optional, List
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
    label: str
    slug: str = field(init=False)
    search_label: str = field(init=False)
    external_id: str
    type: LocationType
    polygon: Optional[List] = None

    def __post_init__(self):
        self.slug = slugify(self.label)
        self.search_label = f"{self.label} ({self.external_id})"

@dataclass_json
@dataclass
class GroupEntity(Entity):
    label: str
    slug: str = field(init=False)
    type: GroupType
    label_search: str = field(init=False)
    location_id: Optional[str] = None
    location: LocationEntity = None

    def __post_init__(self):
        self.slug = slugify(self.label)
        self.label_search = self.label


@dataclass_json
@dataclass
class PositionGroupTypeEntity(Entity):
    label: str
    slug: str = field(init=False)
    group_type: GroupType

    def __post_init__(self):
        self.slug = slugify(self.label)


@dataclass_json
@dataclass
class UserPositionEntity(Entity):
    position_name: str
    group_id: str
    group: GroupEntity
