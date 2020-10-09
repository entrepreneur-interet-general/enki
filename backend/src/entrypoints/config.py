from .serializers import SapeurJsonEncoder


class SapeursConfig(object):
    RESTFUL_JSON = {
        'indent': 2,
        'cls': SapeurJsonEncoder
    }
