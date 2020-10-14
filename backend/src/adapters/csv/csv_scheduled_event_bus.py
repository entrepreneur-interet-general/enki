from ast import copy_location
import asyncio
import logging
import os
from numpy.lib.function_base import copy 

from pandas.api.types import is_datetime64_any_dtype as is_datetime
import pandas as pd
from datetime import datetime
from adapters.csv.csv_helpers import series_to_vehicle_event

from domain.couv_ops.ports.event_bus import InMemoryEventBus
from domain.couv_ops.ports.event_bus import Topic
from heplers.clock import AbstractClock


class CsvError(Exception):
    pass
class Pause(Exception):
    pass
class CsvScheduledEventBus(InMemoryEventBus):
    def __init__(self, clock: AbstractClock,  *, csv_path: str = None, df: pd.DataFrame = None):
        self.clock = clock
        self.df: pd.DataFrame
        if df is not None: 
            self.df = df.copy()
        else:
            if csv_path is None or not os.path.exists(csv_path):
                raise CsvError("Csv_path or DF should be provided")
            self.df = pd.read_csv(csv_path)
        self._sanity_check()
        self.df.index = self.df.timestamp

    def start(self, resync: bool = False):
        now = self.clock.get_now()
        
        if resync: # todo : inplace or not inplace ? rather not,  I guess. 
            offset = pd.Timestamp(now) - self.df.timestamp[0]
            self.df.index += offset
            self.df.timestamp += offset 

        self._last_published_timestamp = self.df.timestamp[0]
        self._previous_now = now

    async def play(self, time_step: float, speed: float = 1):
        self._time_step = time_step
        asyncio.run(self.__async_loop(speed))
        # return asyncio.get_running_loop()

    def _dispatch_event(self, event_series: pd.Series):
        topic: Topic = event_series.topic
        if topic == "vehicule_changed_status":
            event = series_to_vehicle_event(event_series)
            self.publish(event)

    def _next(self, speed : float = 1):
        now = self.clock.get_now()
        ellapsed = now - self._previous_now
        next_timestamp_begins = self._last_published_timestamp
        next_timestamp_ends = next_timestamp_begins + ellapsed * speed
        rows_to_dispatch = self.df[next_timestamp_begins:next_timestamp_ends]
        logging.info(f"\n \n \n rows_to_dispatch: {len(rows_to_dispatch)}\n \n \n ")
        for _, serie in rows_to_dispatch.iterrows():
            self._dispatch_event(serie)

        self._previous_now = now
        self._last_published_timestamp = next_timestamp_ends

    async def __async_next(self, speed : float):
        logging.info("\n \n \n About to sleep \n \n \n ")
        await self.clock.sleep(self._time_step) #asyncio.sleep(self._timespan)
        logging.info("\n \n \n Woken up from sleep \n \n \n ")
        self._next(speed)
        
    async def __async_loop(self, speed: float):
        last_row_timesamp = self.df.index[-1]
        while last_row_timesamp > self._last_published_timestamp:
            await self.__async_next(speed)

    def _sanity_check(self):
        self._has_required_columns()
        self._timestamps_is_datetime()
        self._timestamps_is_monotonic()

    def _has_required_columns(self) -> None:
        required_columns = { "uuid", "timestamp", "topic" }
        columns = set(self.df.columns)
        missing_columns = required_columns - columns
        if missing_columns:
            raise CsvError(f"Some columns are missing : {missing_columns}")

    def _timestamps_is_datetime(self):
        if not is_datetime(self.df.timestamp):
            try:
                self.df.timestamp = pd.to_datetime(self.df.timestamp)
            except Exception:
                raise CsvError("Timestamp cannot be converted to datetime")
        
    def _timestamps_is_monotonic(self):
        if not self.df.timestamp.is_monotonic:
            self.df.sort_values("timestamp", inplace=True)
