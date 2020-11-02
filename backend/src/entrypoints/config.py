from .repositories.repositories import Repositories, InMemoryRepository, SQLRepository, REPOSITORY_TYPES
from .serializers import SapeurJsonEncoder
import os


class SapeursConfig(object):
    RESTFUL_JSON = {
        'indent': 2,
        'cls': SapeurJsonEncoder
    }
    REPO_INFRA: str = os.environ.get('REPOSITORIES', InMemoryRepository.name)
    SGE_HUB_BASE_URI: str = os.environ.get('SGE_HUB_BASE_URI', 'http://localhost:9090')
    SGE_REF_BASE_URI: str = os.environ.get('SGE_REF_BASE_URI', 'http://localhost:10010')
    CONTEXT_FACTORY: Repositories = REPOSITORY_TYPES[REPO_INFRA]
