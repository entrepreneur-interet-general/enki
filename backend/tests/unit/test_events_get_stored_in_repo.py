from domain.couv_ops.entities.vehicule_event_entity import VehiculeEventEntity
from domain.couv_ops.ports.vehicule_repository import InMemoryVehiculeEventRepository
from domain.couv_ops.use_cases.update_couvops_on_event import update_couvops_on_event


def test_update_couvops_on_event():
    # create event
    repo = InMemoryVehiculeEventRepository()
    update_couvops_on_event()
    assert repo.vehicule_events == []
    