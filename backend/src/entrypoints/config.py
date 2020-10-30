from .repositories.repositories import Repositories, InMemoryRepository, SQLRepository, REPOSITORY_TYPES
from .serializers import SapeurJsonEncoder
import os


class SapeursConfig(object):
    RESTFUL_JSON = {
        'indent': 2,
        'cls': SapeurJsonEncoder
    }
    REPO_INFRA: str = os.environ.get('REPOSITORIES', InMemoryRepository.name)
    CONNECT_SGE: bool = os.environ.get('CONNECT_SGE', 'false') == 'true'
    LOCAL_PG_URI: str = os.environ.get('DATABASE_URI')
    CONTEXT_FACTORY: Repositories = REPOSITORY_TYPES[REPO_INFRA]
