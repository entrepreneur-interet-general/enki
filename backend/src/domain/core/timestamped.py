import asyncio

from dataclasses import dataclass, field
from datetime import datetime
import abc


class AbstractClock(abc.ABC):
    can_wake_up: bool = True

    @abc.abstractclassmethod
    def get_now(self) -> datetime:
        raise NotImplementedError

    @abc.abstractclassmethod
    async def sleep(self, delay: float):
        raise NotImplementedError


class RealClock(AbstractClock):
    def get_now(self) -> datetime:
        return datetime.now()

    async def sleep(self, delay: float):
        await asyncio.sleep(delay)


class TimeStamped:
    created_at: datetime
    updated_at: datetime

    def __init__(self, clock: AbstractClock):
        self.clock = clock
        self.created_at: datetime = self.clock.get_now()
        self.updated_at: datetime = self.clock.get_now()
