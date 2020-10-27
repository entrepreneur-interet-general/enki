import json
from datetime import date, datetime

from flask import make_response
from domain.affairs.cisu.entities.commons.cisu_enum import CisuEnum


class SapeurJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return str(obj)
            elif isinstance(obj, date):
                return str(obj)
            elif isinstance(obj, CisuEnum):
                return str(obj)
            elif obj is None:
                return None
            return json.JSONEncoder.default(self, obj)
        except TypeError as e:
            raise TypeError(obj)


def custom_json_output(data, code, headers=None):
    dumped = json.dumps({k: v for k, v in data.items() if v is not None}, cls=SapeurJsonEncoder)
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
