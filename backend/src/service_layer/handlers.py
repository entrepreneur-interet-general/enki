from flask import current_app

from domain.core import events
from adapters.notifications import email, sms
from adapters.http.sge import SgeHelper


def send_affair_created_email_notification(event: events.AffairCreatedEvent):
    email.send(
        'mairie@chelles.com',
        f'{event.data.eventId}',
        f'{event.data.primaryAlert.alertCode.whatsHappen.label}'
    )


def send_affair_created_sms_notification(event: events.AffairCreatedEvent):
    sms.send(
        'mairie@chelles.com',
        f'{event.data.eventId}',
        f'{event.data.primaryAlert.alertCode.whatsHappen.label}'
    )


def send_ack_message_to_sge_on_affair_received(event: events.AffairCreatedEvent):
    response = SgeHelper.send_ack_to_sge(event=event)
    current_app.logger.info(f"response {response}")
    current_app.logger.info(f"response {response.status_code}")
    current_app.logger.info(f"response {response.json()}")
