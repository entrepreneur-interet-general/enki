from adapters.minio.resource_content_repository import MinioResourceContentRepository
from domain.core.ports.event_bus import AbstractEventBus, InMemoryEventBus
from entrypoints.commons.specs import APISpecExt
from entrypoints.config import EnkiConfig
from heplers.clock import RealClock
from flask_oidc import OpenIDConnect


api_spec = APISpecExt()
clock = RealClock()
event_bus: AbstractEventBus = InMemoryEventBus()
minio = MinioResourceContentRepository.from_config(EnkiConfig())
oidc = OpenIDConnect()
