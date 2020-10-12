from dataclasses import dataclass
from pandas import Timestamp

from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData
from domain.couv_ops.ports.event_bus import TopicVehiculeChangedStatus

@dataclass
class VehiculeEvent():
    timestamp: Timestamp
    topic: TopicVehiculeChangedStatus
    uuid: str
    data: VehiculeEventData
