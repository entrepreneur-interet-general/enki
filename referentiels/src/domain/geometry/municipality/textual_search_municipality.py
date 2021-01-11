from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass
class Location:
    longitude: float
    latitude: float


@dataclass
class Address:
    libelle: str
    codeInsee: str
    ville: str


@dataclass_json
@dataclass
class SearchMunicipalityEntity:
    """
    """

    id: str
    type: str
    score: float
    adresse: Address
    localisation: Location
