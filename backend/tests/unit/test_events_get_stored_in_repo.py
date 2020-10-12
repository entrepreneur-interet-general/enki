from pandas._libs.tslibs import Timestamp
from uuid import uuid4

from domain.couv_ops.entities.vehicule_event_entity import VehiculeEventEntity
from domain.couv_ops.events.vehicule_events import VehiculeEvent
from domain.couv_ops.ports.vehicule_repository import InMemoryVehiculeEventRepository
from domain.couv_ops.use_cases.update_couvops_on_event import UpdateCouvopsOnEvent
from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData


def test_update_couvops_on_event():
    # create event
    timestamp = Timestamp('2000-01-01T00')
    raw_vehicule_id = 42
    raw_intervention_id = 896
    status = 'selected'
    is_available = False
    raw_status = 'Sélectionné'
    home_area = 'PTE_CHAMP'
    role = 'vehicule_rescue'
    uuid = str(uuid4())
    incoming_vehicule_event_data = VehiculeEventData(
        raw_vehicule_id=raw_vehicule_id,
        raw_intervention_id=raw_intervention_id, 
        status=status,
        is_available=is_available,
        raw_status=raw_status,
        home_area=home_area,
        role=role
        )        
    incoming_vehicule_event = VehiculeEvent(
        timestamp=timestamp, 
        kind='vehicule_changed_status',
        uuid=uuid,
        data=incoming_vehicule_event_data
    )   
    expected_vehicule_event_entity = VehiculeEventEntity(
        timestamp=timestamp, 
        uuid=uuid,
        data=incoming_vehicule_event_data
        )   
    repo = InMemoryVehiculeEventRepository()
    update_couvops_on_event = UpdateCouvopsOnEvent(vehicule_repo=repo)
    update_couvops_on_event.execute(event=incoming_vehicule_event)
    assert repo.vehicule_events == [expected_vehicule_event_entity]
    