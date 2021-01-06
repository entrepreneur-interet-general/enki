from domain.evenements.command import CreateEvenement
from domain.evenements.service import EvenementService
from domain.tasks.command import CreateTask, CreateTag
from domain.tasks.services.tag_service import TagService
from domain.tasks.services.task_service import TaskService
from domain.tasks.services.information_service import InformationService
from service_layer.unit_of_work import AbstractUnitOfWork


def create_evenement(command: CreateEvenement, uow: AbstractUnitOfWork):
    return EvenementService.add_evenement(data=command.data, uow=uow)


def create_task(command: CreateTask, uow: AbstractUnitOfWork):
    return TaskService.add_task(
        uuid=command.data["uuid"],
        title=command.data["title"],
        description=command.data["description"],
        uow=uow)


def create_tag(command: CreateTag, uow: AbstractUnitOfWork):
    return TagService.add_tag(
        uuid=command.data["uuid"],
        title=command.data["title"],
        uow=uow)


def create_information(command: CreateTag, uow: AbstractUnitOfWork):
    return InformationService.add_information(
        uuid=command.data["uuid"],
        title=command.data["title"],
        description=command.data["description"],
        uow=uow)