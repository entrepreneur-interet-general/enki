from flask import current_app
import smtplib
from email.message import EmailMessage


def send(*args):
    current_app.logger.info(f'SENDING EMAIL: {args}', )

    msg = EmailMessage()
    msg.set_content("This is and email")

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = f'Une nouvelle intervention a commencé, voici son identifiant {args[1]}'
    msg['From'] = current_app.config["FROM_EMAIL"]
    msg['To'] = args[0]

    s = smtplib.SMTP('mailhog:1025')
    s.send_message(msg)
    s.quit()
