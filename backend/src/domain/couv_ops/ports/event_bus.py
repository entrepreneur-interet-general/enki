import abc 
from dataclasses import dataclass
from pandas import Timestamp
from typing import Any, Dict, List, Literal, TypedDict, Union, Callable

from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData

class InvalidTopic(Exception):
    pass

TopicVehiculeChangedStatus = Literal['vehicule_changed_status']
Topic = Union[TopicVehiculeChangedStatus]
Data = Union[VehiculeEventData]
EventCallback = Callable[[Any], None]

@dataclass
class Event():
    timestamp: Timestamp
    topic: Topic
    uuid: str
    data: Dict

class DictWithKeysDataEvent(TypedDict):
    data: Any  #  Should be Data
    event: Any # Should be Event

@dataclass
class VehiculeEvent(Event):
    topic: TopicVehiculeChangedStatus
    data: VehiculeEventData

# Event = Union[VehiculeEvent]

class AbstractEventBus(abc.ABC):
    @abc.abstractclassmethod
    def subscribe(self, topic: Topic, callback: EventCallback) -> None:
        raise NotImplementedError()

Subscriptions = Dict[Topic, List[EventCallback]]

class InMemoryEventBus(AbstractEventBus):
    _subscriptions : Subscriptions = {'vehicule_changed_status': []}

    def subscribe(self, topic: Topic, callback: EventCallback) -> None:
        # if not isinstance(topic, Topic):
        #     raise InvalidTopic
        self._subscriptions[topic].append(callback)
        
    def publish(self, event: Event) -> None:
        for callback in self._subscriptions[event.topic]:
            callback(event)

topic_to_types :  Dict[Topic, DictWithKeysDataEvent] = {
    'vehicule_changed_status': {
            'data':  VehiculeEventData,
            'event':  VehiculeEvent,
        }
    }
        