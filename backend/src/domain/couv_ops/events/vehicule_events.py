from dataclasses import dataclass
from pandas import Timestamp
from typing import Literal, TypedDict, Union

from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData

@dataclass
class VehiculeEvent():
    timestamp: Timestamp
    kind: str
    uuid: str
    data: VehiculeEventData
