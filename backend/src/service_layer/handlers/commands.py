from domain.evenements.command import CreateEvenement
from domain.evenements.service import EvenementService
from domain.messages.command import CreateTag, CreateMessage, CreateResource
from domain.messages.services.resource_service import ResourceService
from domain.messages.services.tag_service import TagService
from domain.messages.services.message_service import MessageService
from domain.users.command import CreateUser, CreateContact, CreateInvitation
from domain.users.services.contact_service import ContactService
from domain.users.services.invitation_service import InvitationService
from domain.users.services.user_service import UserService
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


def create_user(command: CreateUser, uow: AbstractUnitOfWork):
    return UserService.add_user(
        data=command.data,
        uow=uow)


def create_contact(command: CreateContact, uow: AbstractUnitOfWork):
    return ContactService.add_contact(
        data=command.data,
        uow=uow)


def create_invitation(command: CreateInvitation, uow: AbstractUnitOfWork):
    return InvitationService.create_invitation(
        data=command.data,
        uow=uow
    )
