import abc
import asyncio

from datetime import datetime, timedelta

class AbstractClock(abc.ABC):
    can_wake_up: bool = True

    @abc.abstractclassmethod
    def get_now(self) -> datetime:
        raise NotImplementedError

    @abc.abstractclassmethod
    async def sleep(self, delay: float):
        raise NotImplementedError


class CustomClock(AbstractClock):
    next_date: datetime = datetime.now()
    awaken_event: asyncio.Event

    def get_now(self) -> datetime:
        return self.next_date

    def set_next_date(self, date: datetime):
        self.next_date = date

    def add_seconds(self, delay: float):
        self.next_date += timedelta(seconds=delay)
        
    async def sleep(self, delay: float):
        await self.awaken_event.wait()
        self.can_wake_up = False

    def set_awaken_event(self, awaken_event: asyncio.Event):
      self.can_wake_up = True
      self.awaken_event = awaken_event   

    async def wake_up(self): 
      self.awaken_event.set()
  

class RealClock(AbstractClock):
  def get_now(self) -> datetime:
      return datetime.now()

  async def sleep(self, delay: float):
      await asyncio.sleep(delay)
      