from flask import current_app

from adapters.http.sge import SgeHelper
from adapters.notifications import email, sms
from domain.core import events
from domain.evenements.services.message_service import MessageService
from domain.users.entities.user import UserEntity
from domain.users.services.contact_service import ContactService
from service_layer.unit_of_work import AbstractUnitOfWork


def send_affair_created_email_notification(event: events.AffairCreatedEvent, **kwargs):
    email.send(
        'mairie@chelles.com',
        f'{event.data.eventId}',
        f'{event.data.primaryAlert.alertCode.whatsHappen.label}'
    )


def send_affair_created_sms_notification(event: events.AffairCreatedEvent, **kwargs):
    sms.send(
        'mairie@chelles.com',
        f'{event.data.eventId}',
        f'{event.data.primaryAlert.alertCode.whatsHappen.label}'
    )


def send_ack_message_to_sge_on_affair_received(event: events.AffairCreatedEvent, **kwargs):
    response = SgeHelper.send_ack_to_sge(event=event)
    current_app.logger.info(f"response {response}")
    current_app.logger.info(f"response {response.status_code}")
    current_app.logger.info(f"response {response.json()}")


def create_contact_from_user(event: events.UserCreatedEvent, uow: AbstractUnitOfWork):
    user: UserEntity = event.data
    ContactService.add_contact_from_user(user=user, uow=uow)


def create_message_from_meeting(event: events.MeetingCreatedEvent, uow: AbstractUnitOfWork):
    MessageService.add_message_from_meeting(meeting=event.data, uow=uow)

def create_message_from_affair(event: events.AffairCreatedEvent, uow: AbstractUnitOfWork):
    MessageService.add_message_from_affair(affair=event.data, uow=uow)


def send_email_at_participants(event: events.MeetingCreatedEvent, uow: AbstractUnitOfWork):
    raise NotImplementedError
