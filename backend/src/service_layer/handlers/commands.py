from minio.datatypes import Upload

from domain.evenements.command import CreateEvenement
from domain.evenements.service import EvenementService
from domain.messages.command import CreateTag, CreateMessage, CreateResource
from domain.messages.services.resource_service import ResourceService
from domain.messages.services.tag_service import TagService
from domain.messages.services.message_service import MessageService
from service_layer.unit_of_work import AbstractUnitOfWork


def create_evenement(command: CreateEvenement, uow: AbstractUnitOfWork):
    return EvenementService.add_evenement(data=command.data, uow=uow)


def create_message(command: CreateMessage, uow: AbstractUnitOfWork):
    return MessageService.add_message(
        data=command.data,
        uow=uow)


def create_tag(command: CreateTag, uow: AbstractUnitOfWork):
    return TagService.add_tag(
        data=command.data,
        uow=uow)

def create_resource(command: CreateResource, uow: AbstractUnitOfWork):
    return ResourceService.add_resource(
        data=command.data,
        uow=uow)