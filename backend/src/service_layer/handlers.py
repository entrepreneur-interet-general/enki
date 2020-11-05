from domain.core import events
from adapters.notifications import email, sms
from adapters.http.sge import SgeHelper


def send_affair_created_email_notification(event: events.AffairCreatedEvent):
    email.send(
        'mairie@chelles.com',
        f'Affair {event.uuid} was created',
        f'{event.uuid}'
    )


def send_affair_created_sms_notification(event: events.AffairCreatedEvent):
    sms.send(
        'mairie@chelles.com',
        f'Affair {event.uuid} was created',
        f'{event.uuid}'
    )


def send_ack_message_to_sge_on_affair_received(event: events.AffairCreatedEvent):
    return SgeHelper.send_ack_to_sge(event=event)
