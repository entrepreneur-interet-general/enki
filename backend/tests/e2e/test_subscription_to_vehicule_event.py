from tests.factories.vehicule_event_factory import make_vehicule_event, make_vehicule_event_data, make_vehicule_event_entity
from domain.couv_ops.events.events import VehiculeEvent
from domain.couv_ops.ports.event_bus import InMemoryEventBus
from domain.couv_ops.ports.vehicule_event_repository import InMemoryVehiculeEventRepository
from domain.couv_ops.use_cases.update_couvops import UpdateCouvops


def test_inmemory_subscription_to_vehicule_event():
    event_bus = InMemoryEventBus()
    vehicule_event_repo = InMemoryVehiculeEventRepository()
    use_case = UpdateCouvops(vehicule_event_repo=vehicule_event_repo)
    event_bus.subscribe(topic='vehicule_changed_status',
                        callback=use_case.execute)
    incoming_vehicule_event_data = make_vehicule_event_data()
    incoming_vehicule_event = make_vehicule_event(data=incoming_vehicule_event_data)
    expected_vehicule_event_entity = make_vehicule_event_entity(data=incoming_vehicule_event_data)
    # publish event
    event_bus.publish(event=incoming_vehicule_event)
    #  check that repo contains the data just published 
    assert vehicule_event_repo.vehicule_events == [expected_vehicule_event_entity]