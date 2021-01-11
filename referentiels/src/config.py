from typing import Optional

from .entrypoints.repositories.repositories import Repositories, InMemoryRepositories, REPOSITORY_TYPES
from .entrypoints.serializer import ReferentielsJsonEncoder
import os


class ReferentielConfig(object):
    RESTFUL_JSON = {
        'indent': 2,
        'cls': ReferentielsJsonEncoder
    }
    SECRET_KEY = 'SomethingNotEntirelySecret'
    REPO_INFRA: str = os.environ.get('REPOSITORIES', InMemoryRepositories.name)
    DATABASE_URI: str = os.environ.get("DATABASE_URI", "sqlite:///:memory:")
    CONTEXT_FACTORY: Repositories = REPOSITORY_TYPES[REPO_INFRA]
