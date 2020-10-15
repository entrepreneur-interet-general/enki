import pandas as pd
from dataclasses import asdict

from domain.couv_ops.events.events import VehiculeEvent
from domain.couv_ops.ports.event_bus import Event
from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData
from domain.couv_ops.ports.event_bus import Topic, topic_to_types

def event_to_series(event: Event) -> pd.Series:
    event_dict = asdict(event.data)
    event_dict['uuid'] = event.uuid
    event_dict['timestamp'] = event.timestamp
    event_dict['topic'] = event.topic
    return pd.Series(event_dict)

def series_to_event(topic: Topic, series: pd.Series) -> Event:
    data_dict = dict(series[~series.index.isin(["timestamp", "uuid", "topic"])])
    if topic not in topic_to_types:
        raise ValueError(f'Unknown topic {topic}')
    EventDataType = topic_to_types.get(topic)['data']
    EventType = topic_to_types.get(topic)['event']
    data = EventDataType(**data_dict)
    return EventType(series.timestamp, series.topic, series.uuid, data)
