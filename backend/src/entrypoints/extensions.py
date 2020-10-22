from entrypoints.commons.specs import APISpecExt
from entrypoints.repositories import Repositories
from heplers.clock import RealClock

repositories = Repositories()
api_spec = APISpecExt()
clock = RealClock()
