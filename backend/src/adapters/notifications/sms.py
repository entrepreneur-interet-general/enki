import os
from twilio.rest import Client
from flask import current_app


def send(*args):
    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=f'Une nouvelle intervention a commencé, voici son identifiant {args[1]}',
        from_=current_app.config['FROM_TEL_NUMBER'],
        to='+33 7 72 32 41 57'
    )

    print(message.sid)

    current_app.logger.info(f'SENDING SMS with {message.sid}', )
