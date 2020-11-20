import json
from datetime import date, datetime


class ReferentielsJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return str(obj)
            elif isinstance(obj, date):
                return str(obj)
            else:
                return json.JSONEncoder.default(self, obj)
        except TypeError as e:
            raise TypeError(obj)