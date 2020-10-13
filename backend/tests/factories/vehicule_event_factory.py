from dataclasses import asdict
import random
from typing import Optional
from uuid import uuid4
from faker import Faker
from pandas._libs.tslibs import Timestamp
from domain.couv_ops.entities.vehicule_event_entity import VehiculeEventEntity
from domain.couv_ops.events.events import VehiculeEvent

from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData, vehicule_status_options, \
    vehicule_available_status_options, vehicule_role_options, VehiculeRole, VehiculeStatus

fake = Faker()

default_timestamp = Timestamp('2020-01-01T12')
default_uuid = str(uuid4())

def make_vehicule_event_data(
        raw_vehicule_id: int = None,
        raw_intervention_id: int = None,
        status: VehiculeStatus = None, 
        is_available: bool = None,
        raw_status: str = None,
        home_area: str = None,
        role: VehiculeRole = None,
) -> VehiculeEventData:
    if status and status not in vehicule_status_options:
        raise ValueError(f'Provided status not in {vehicule_status_options}')
    raw_vehicule_id = raw_vehicule_id or fake.pyint() 
    raw_intervention_id = raw_intervention_id or fake.pyint()
    status = status or random.choice(vehicule_status_options)
    is_available =  is_available or status in vehicule_available_status_options
    raw_status = raw_status or 'some raw status'
    home_area = home_area or 'some home area' # warnings: this should be an id linked to the map 
    role = role or random.choice(vehicule_role_options)
    vehicule_event_data = VehiculeEventData(
        raw_vehicule_id=raw_vehicule_id,
        raw_intervention_id=raw_intervention_id, 
        status=status,
        is_available=is_available,
        raw_status=raw_status,
        home_area=home_area,
        role=role
        )   
    return vehicule_event_data
    
def make_vehicule_event(
        timestamp: Timestamp = None, 
        uuid: str = None, 
        data: VehiculeEventData = None
    ) -> VehiculeEvent:
    data = data or make_vehicule_event_data()
    vehicule_event_data = make_vehicule_event_data(**asdict(data))
    timestamp = timestamp or default_timestamp
    uuid = uuid or default_uuid
    return VehiculeEvent(
        timestamp=timestamp, 
        topic='vehicule_changed_status',
        uuid=uuid, 
        data=vehicule_event_data)

def make_vehicule_event_entity(
        timestamp: Timestamp = None, 
        uuid: str = None, 
        data: VehiculeEventData = None
    ) -> VehiculeEventEntity:
    data = data or make_vehicule_event_data()
    vehicule_event_data = make_vehicule_event_data(**asdict(data))
    timestamp = timestamp or default_timestamp
    uuid = uuid or default_uuid
    return VehiculeEventEntity(
        timestamp=timestamp, 
        uuid=uuid, 
        data=vehicule_event_data)