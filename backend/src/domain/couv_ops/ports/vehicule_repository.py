import abc
from typing import List, Union

from domain.couv_ops.entities.vehicule_event_entity import VehiculeEventEntity


VehiculeEventsList = List[VehiculeEventEntity]

class AlreadyExistingVehiculeEventUuid(Exception):
    pass

class NotFoundTask(Exception):
  pass

class AbstractVehiculeEventRepository(abc.ABC):
    def add(self, vehicule_event_entity: VehiculeEventEntity) -> None:
        if self._match_uuid(vehicule_event_entity.uuid):
            raise AlreadyExistingVehiculeEventUuid()
        self._add(vehicule_event_entity)

    # def get_by_uuid(self, uuid : str) -> VehiculeEventEntity:
    #     matches = self._match_uuid(uuid)
    #     if not matches:
    #         raise NotFoundTask
    #     return matches[0]

    # @abc.abstractclassmethod
    # def get_all(self) -> TasksList:
    #     raise NotImplementedError

    @abc.abstractclassmethod
    def _add(self, task: VehiculeEventEntity) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def _match_uuid(self, uuid: str) -> List[VehiculeEventEntity]:
        raise NotImplementedError



class InMemoryVehiculeEventRepository(AbstractVehiculeEventRepository):
    _events: VehiculeEventsList = []

    def get_all(self) -> VehiculeEventsList:
        return self._events

    def _match_uuid(self, uuid: str) -> List[VehiculeEventEntity]:
        return [task for task in self._events if task.uuid == uuid]

    def _add(self, task: VehiculeEventEntity):
        self._events.append(task)

    # next methods are only for test purposes
    @property
    def vehicule_events(self) -> VehiculeEventsList:
        return self._events

    # def set_tasks(self, tasks: TasksList) -> None:
    #     self._events = tasks