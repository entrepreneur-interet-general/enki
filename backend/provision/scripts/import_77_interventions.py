import json
import os
from tqdm import tqdm
from datetime import datetime, date
import pandas as pd

from elasticsearch import helpers
from elasticsearch import Elasticsearch

from cisu.entities.commons import DateType
from cisu.entities.commons.cisu_enum import CisuEnum
from cisu.entities.commons.common_alerts import AttributeType, Victims
from cisu.entities.commons.location_type import LocationShape
from cisu.factories.edxl_factory import EdxlMessageFactory
from cisu.entities.commons.common_alerts import MainVictim
from cisu.entities.commons.severity import Severity
from cisu.constants.constants import WhatsHappenConstants, HealthMotiveConstants

df_final_mapped = pd.read_csv("data/2019_77_interventions.csv", parse_dates=["DAT_DEB"])
records = df_final_mapped.to_dict(orient="records")

health_motive_constant = HealthMotiveConstants()
whats_happen_constants = WhatsHappenConstants()

AFFAIRS_INDEX_NAME = os.environ.get("AFFAIRS_INDEX_NAME")


def build_edxl_from_record(record):
    try:
        return EdxlMessageFactory.build_ack_from_simple_infos(
            created_at=record["DAT_DEB"].to_pydatetime(),
            lat=record["latitude"],
            lon=record["longitude"],
            address=record["ADDRESS"],
            severity=Severity.UNKNOWN,
            whatsHappen=whats_happen_constants.get_by_code(code=record['Nature de faits']),
            victims=Victims(count=1, mainVictim=MainVictim.ADULT, comment=None),
            locationKind=None,
            healthMotive=health_motive_constant.get_by_code(code=record["Pathologie"]),
            riskThreat=None
        )
    except Exception as e:
        print(e)
        pass


class CisuAffairEncoder(json.JSONEncoder):
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
            return str(obj)


ELASTIC_HOST = os.environ.get("ELASTIC_HOST")
ELASTIC_PORT = os.environ.get("ELASTIC_PORT")
ELASTIC_USERNAME = os.environ.get("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD")

client = Elasticsearch([f"{ELASTIC_HOST}:{ELASTIC_PORT}"], http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD))

print(f"Ping client : {client.ping()}")

with open("templates/affairs.json") as f:
    affair_mapping = json.load(f)

response = client.indices.create(
    index=AFFAIRS_INDEX_NAME,
    body=affair_mapping,
    ignore=400  # ignore 400 already exists code
)

affairs = [edxl.resource.message.choice.to_dict()
           for edxl in [build_edxl_from_record(record) for record in tqdm(records)] if edxl]

print(f"{len(affairs)} affairs were created")
for affair in tqdm(affairs):
    lat = affair["eventLocation"]["coord"]["lat"]
    lon = affair["eventLocation"]["coord"]["lon"]
    affair["location"] = {
        "lat": float(lat),
        "lon": float(lon)
    }


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


for chunk in chunks(affairs, 5000):
    actions = [
        {
            "_id": affair["eventId"],
            "_index": AFFAIRS_INDEX_NAME,
            "_source": json.loads(json.dumps(affair, cls=CisuAffairEncoder, ))
        }
        for affair in tqdm(chunk)
    ]

    response = helpers.bulk(client, actions)
    print(response)
