import os
from twilio.rest import Client
from flask import current_app


def send(*args):
    to_email, intervention_id, what_happens_label = args
    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    client = Client(
        account_sid,
        auth_token
    )

    message = client.messages.create(
        body=f"Une nouvelle intervention a commencé, pour plus "
             f"d'informations Veuillez trouver "
             f"{current_app.config['ENKI_FRONT_BASE_URI']}/detail-intervention/{args[2]}",
        from_=current_app.config['FROM_TEL_NUMBER'],
        to=current_app.config['FROM_TEL_NUMBER'],
    )

    current_app.logger.info(f'SENDING SMS with {message.sid}')

