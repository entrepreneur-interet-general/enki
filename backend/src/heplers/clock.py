import abc
import asyncio
from asyncio.tasks import Task
from datetime import datetime, timedelta
import logging
from typing import Union

class AbstractClock(abc.ABC):
    @abc.abstractclassmethod
    def get_now(self) -> datetime:
        raise NotImplementedError

    @abc.abstractclassmethod
    async def sleep(self, delay: float) -> None:
        raise NotImplementedError


class CustomClock(AbstractClock):
    is_sleeping: bool = True
    next_date: datetime = datetime.now()
    _sleeping_task: Task

    def get_now(self) -> datetime:
        return self.next_date

    def set_next_date(self, date: datetime):
        self.next_date = date

    def add_seconds(self, delay: float):
        self.next_date += timedelta(seconds=delay)

    async def _set_sleeping_task(self, delay: float):
        try: 
            await asyncio.sleep(delay)
        except asyncio.CancelledError:
            logging.info('Sleep was cancelled')
            raise
    
    def sleep(self, delay: float):
        self._sleeping_task = asyncio.create_task(self._set_sleeping_task(delay))

    @property
    def sleeping_task(self):
        return self._sleeping_task

        # logging.info(f'Just before the while {self.is_sleeping}')
        # while self.is_sleeping:
        #     pass
        # logging.info('I am awake, out of while !')


    async def awake_sleep(self):
        self.is_sleeping = False

# class AbstractSleeper(abc.ABC):
#     @abc.abstractclassmethod
#     async def wait(self) -> None:
#         raise NotImplementedError

# class InstantaneousSleeper(AbstractSleeper):
#     async def wait(self) -> None