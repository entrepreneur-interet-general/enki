from domain.couv_ops.entities.vehicule_event_entity import VehiculeEventEntity
from domain.couv_ops.events.events import VehiculeEvent
from domain.couv_ops.ports.vehicule_event_repository import InMemoryVehiculeEventRepository
from domain.couv_ops.use_cases.update_couvops import UpdateCouvops
from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData
from tests.factories.vehicule_event_factory import make_vehicule_event, make_vehicule_event_data, make_vehicule_event_entity

def test_update_couvops():
    # create event
    status = 'selected'

    incoming_vehicule_event_data = make_vehicule_event_data(status=status)
    assert not incoming_vehicule_event_data.is_available
    uuid = 'my uuid'
    incoming_vehicule_event = make_vehicule_event(uuid=uuid, data=incoming_vehicule_event_data)
    expected_vehicule_event_entity = make_vehicule_event_entity(uuid=uuid, data=incoming_vehicule_event_data)
 
    repo = InMemoryVehiculeEventRepository()
    update_couvops = UpdateCouvops(vehicule_event_repo=repo)
    update_couvops.execute(event=incoming_vehicule_event)
    assert repo.vehicule_events == [expected_vehicule_event_entity]
    