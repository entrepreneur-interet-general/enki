import json
from datetime import date, datetime

from flask import make_response

from cisu.entities.commons import DateType
from cisu.entities.commons.cisu_enum import CisuEnum
from cisu.entities.commons.common_alerts import AttributeType, Victims
from cisu.entities.commons.location_type import LocationShape
from domain.tasks.entities.event_entity import Severity
from domain.tasks.entities.task_entity import TaskType


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
            elif isinstance(obj, TaskType):
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


def custom_json_output(data, code, headers=None):
    dumped = json.dumps({k: v for k, v in data.items() if v is not None}, cls=EnkiJsonEncoder)
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
