from datetime import datetime
from heplers.clock import AbstractClock


class TimeStamped:
    created_at: datetime
    updated_at: datetime

    def __init__(self, clock: AbstractClock):
        self.clock = clock
        self.created_at: datetime = self.clock.get_now()
        self.updated_at: datetime = self.clock.get_now()
