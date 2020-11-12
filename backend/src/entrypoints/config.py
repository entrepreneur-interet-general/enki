from typing import Optional

from .repositories.repositories import Repositories, InMemoryRepositories, REPOSITORY_TYPES
from .serializers import SapeurJsonEncoder
import os


class SapeursConfig(object):
    RESTFUL_JSON = {
        'indent': 2,
        'cls': SapeurJsonEncoder
    }
    REPO_INFRA: str = os.environ.get('REPOSITORIES', InMemoryRepositories.name)
    SGE_HUB_BASE_URI: str = os.environ.get('SGE_HUB_BASE_URI',
                                           'http://docker.for.mac.localhost:9090')
    SGE_REF_BASE_URI: str = os.environ.get('SGE_REF_BASE_URI',
                                           'http://docker.for.mac.localhost:10010')
    DATABASE_URI: str = os.environ.get("DATABASE_URI", "sqlite:///:memory:")
    ENKI_SGE_ID = "sgc-enki"
    ENKI_SGE_ADDRESS = "sge:sgc-enki"
    CONTEXT_FACTORY: Repositories = REPOSITORY_TYPES[REPO_INFRA]
    TWILIO_ACCOUNT_SID: Optional[str] = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN: Optional[str] = os.environ.get('TWILIO_AUTH_TOKEN')
    FROM_EMAIL = "enki@ansc.fr"
    FROM_TEL_NUMBER = "+13345084085"
    TO_TEL_NUMBER = "+33772324157"
    ENKI_FRONT_BASE_URI: str = os.environ.get(
        'ENKI_FRONT_BASE_URI',
        'http://localhost:4200'
    )

    ELASTIC_HOST = os.environ.get('ELASTIC_USER', "http://elasticsearch:9200")
    ELASTIC_USER = os.environ.get('ELASTIC_HOST', "elastic")
    ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD', "changeme")




