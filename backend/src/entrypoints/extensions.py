from domain.core.ports.event_bus import AbstractEventBus, InMemoryEventBus
from entrypoints.commons.specs import APISpecExt
from heplers.clock import RealClock
api_spec = APISpecExt()
clock = RealClock()
event_bus: AbstractEventBus = InMemoryEventBus()
