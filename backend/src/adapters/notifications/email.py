import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import current_app
import smtplib
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))

def send(*args):
    current_app.logger.info(f'SENDING EMAIL: {args}', )
    to_email, intervention_id, what_happens_label = args
    from_email = current_app.config["FROM_EMAIL"]

    template = env.get_template('email.html')
    #intervention_url = f"{current_app.config['ENKI_FRONT_BASE_URI']}/detail-intervention/{intervention_id}"
    intervention_url = f"{current_app.config['ENKI_FRONT_BASE_URI']}/liste-interventions"
    body_content = template.render(
        intervention_url=intervention_url,
        what_happens_label=what_happens_label
    )
    message = MIMEMultipart()
    message.attach(MIMEText(body_content, "html"))
    message['Subject'] = 'Une nouvelle intervention a commencé sur votre communne'
    message['From'] = from_email
    message['To'] = to_email
    msg_body = message.as_string()

    s = smtplib.SMTP('mailhog:1025')
    s.sendmail(from_email, to_email, msg_body)
    s.quit()
