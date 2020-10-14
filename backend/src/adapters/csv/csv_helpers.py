import pandas as pd
from dataclasses import asdict
from domain.couv_ops.events.events import VehiculeEvent

from domain.couv_ops.ports.event_bus import Event
from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData


def event_to_series(event: Event) -> pd.Series:
    event_dict = asdict(event.data)
    event_dict['uuid'] = event.uuid
    event_dict['timestamp'] = event.timestamp
    event_dict['topic'] = event.topic
    return pd.Series(event_dict)

def series_to_vehicle_event(series: pd.Series) -> VehiculeEvent:
    data_dict = dict(series[~series.index.isin(["timestamp", "uuid", "topic"])])
    data = VehiculeEventData(**data_dict)
    return VehiculeEvent(series.timestamp, series.topic, series.uuid, data)
