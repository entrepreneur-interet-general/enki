from dataclasses import dataclass

import abc
from typing import TypedDict 
from pandas._libs.tslibs import Timestamp

from domain.couv_ops.events.vehicule_events import VehiculeEvent
from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData

@dataclass
class EventEntity(abc.ABC):
    timestamp: Timestamp
    data: TypedDict
    uuid: str

class VehiculeEventEntity(EventEntity):
    data: VehiculeEventData