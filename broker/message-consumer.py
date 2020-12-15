import json
from dataclasses import dataclass
from datetime import datetime, date
from json import loads
from cisu.entities.commons import DateType, Severity
from cisu.entities.commons.cisu_enum import CisuEnum
from cisu.entities.commons.common_alerts import AttributeType, Victims
from cisu.entities.commons.location_type import LocationShape
from cisu.entities.cisu_entity import CreateEvent
from cisu.entities.edxl_entity import EdxlEntity
from dataclasses_json import dataclass_json
from kafka import KafkaConsumer
import xml.dom.minidom
from elasticsearch import Elasticsearch
import os
import time

time.sleep(15)
print("Start consuming")

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
ELASTIC_URL = os.environ.get("ELASTIC_URL", "localhost:9200")
print(f"Start listening kafka on {KAFKA_BROKER_URL}")


class EnkiJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return str(obj)
            elif isinstance(obj, date):
                return str(obj)
            elif isinstance(obj, DateType):
                return str(obj)
            elif isinstance(obj, CisuEnum):
                return str(obj)
            elif isinstance(obj, Severity):
                return str(obj)
            elif isinstance(obj, LocationShape):
                return str(obj)
            elif isinstance(obj, AttributeType):
                return obj.to_dict()
            elif isinstance(obj, Victims):
                return obj.to_dict()
            elif obj is None:
                return None
            return json.JSONEncoder.default(self, obj)
        except TypeError as e:
            raise TypeError(obj)


@dataclass_json
@dataclass
class AffairEntity(CreateEvent):
    """

    """

    @property
    def uuid(self):
        return self.eventId

    @property
    def location(self):
        return {
            "lat": self.eventLocation.coord.lat,
            "lon": self.eventLocation.coord.lon
        }


consumer = KafkaConsumer(
    'messages',
    bootstrap_servers=[KAFKA_BROKER_URL],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

client = Elasticsearch(hosts=[ELASTIC_URL], http_auth=("elastic", "changeme"))

print(f"Start listening kafka on {KAFKA_BROKER_URL}")
for message in consumer:
    try:
        xml_parsed_from_message = xml.dom.minidom.parseString(message.value["message"]["messageBrut"])
        edxl_message = EdxlEntity.from_xml(xml_parsed_from_message)
        print(edxl_message)
        print("-------------------------------------")
        affair = AffairEntity(**edxl_message.resource.message.choice.to_dict())
        client.index(index="affairs", id=affair.uuid,
                     body=json.dumps(affair.to_dict(), cls=EnkiJsonEncoder, ))
    except Exception as e:
        print(e)
        print("Skiping this error message")
