from domain.core import events
from adapters.notifications import email, sms


def send_affair_created_email_notification(event: events.AffairCreatedEvent):
    email.send(
        'mairie@chelles.com',
        f'Affair {event.uuid} was created',
    )


def send_affair_created_sms_notification(event: events.AffairCreatedEvent):
    sms.send(
        'mairie@chelles.com',
        f'Affair {event.uuid} was created',
    )
