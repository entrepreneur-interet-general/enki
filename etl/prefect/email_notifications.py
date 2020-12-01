import smtplib
from typing import List, Dict

from prefect import task, Flow
from datetime import timedelta, datetime
from prefect.schedules import IntervalSchedule
from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from elasticsearch import Elasticsearch

env = Environment(loader=FileSystemLoader('templates/'))

INTERVAL = timedelta(seconds=5)
INDEX_NAME = "affairs"


def build_client() -> Elasticsearch:
    return Elasticsearch(
        hosts=["localhost:9200"],
        http_auth=("elastic", "changeme")
    )


@task
def fetch_new_interventions() -> List[Dict]:
    client = build_client()
    query_body = {
        "query": {
            "range": {
                "createdAt": {
                    "gte": (datetime.now() - INTERVAL).strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        }
    }

    result = client.search(index=INDEX_NAME, body=query_body)
    return result["hits"]["hits"]


@task
def send_email(intervention_body):
    to_email, from_email = "test@enki.fr", "test@enki.fr"

    template = env.get_template('email.html')
    intervention_url = f"http://localhost:4200/detail-intervention/154515"
    body_content = template.render(
        intervention_url=intervention_url,
        what_happens_label="WhatsHappen"
    )
    message = MIMEMultipart()
    message.attach(MIMEText(body_content, "html"))
    message['Subject'] = intervention_body["_source"]["primaryAlert"]["alertId"]
    message['From'] = from_email
    message['To'] = to_email
    msg_body = message.as_string()

    s = smtplib.SMTP('localhost:1025')
    s.sendmail(from_email, to_email, msg_body)
    s.quit()


with Flow("Send emails on new Interventions", IntervalSchedule(interval=INTERVAL)) as flow:
    interventions = fetch_new_interventions()
    send_email.map(interventions)

flow.run()
