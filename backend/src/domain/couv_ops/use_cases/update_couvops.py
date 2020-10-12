from domain.couv_ops.entities.vehicule_event_entity import VehiculeEventEntity
from domain.couv_ops.events.events import VehiculeEvent
from domain.couv_ops.ports.vehicule_event_repository import AbstractVehiculeEventRepository


class UpdateCouvops:
    def __init__(self, vehicule_event_repo: AbstractVehiculeEventRepository) -> None:
        self.vehicule_repo = vehicule_event_repo

    def execute(self, event: VehiculeEvent) -> None:
        """Store event in repository

        Args:
            event (VehiculeEvent): event published on vehicule change
        """
        vehicule_event_entity = VehiculeEventEntity(
            timestamp=event.timestamp, 
            data=event.data,
            uuid=event.uuid
        )
        self.vehicule_repo.add(vehicule_event_entity)
