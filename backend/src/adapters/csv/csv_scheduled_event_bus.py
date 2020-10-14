import os 

from pandas.api.types import is_datetime64_any_dtype as is_datetime
import pandas as pd
from datetime import datetime
from adapters.csv.csv_helpers import series_to_vehicle_event

from domain.couv_ops.ports.event_bus import InMemoryEventBus
from domain.couv_ops.ports.event_bus import Topic
from heplers.now import AbstractNow

class CsvError(Exception):
    datetime.now()
    pass

class CsvScheduledEventBus(InMemoryEventBus):
    def __init__(self, now: AbstractNow,  *, csv_path: str = None, df: pd.DataFrame = None):
        self.get_now = now.get
        self.df: pd.DataFrame = df 
        if self.df is None:
            if csv_path is None or not os.path.exists(csv_path):
                raise CsvError("Csv_path or DF should be provided")
            self.df = pd.read_csv(csv_path)
        self._sanity_check()

    def start(self, time_step: float):
        still_has_rows = not self.df.empty
        self.current_cursor: int = 0
        first_event_series = self.df.iloc[0]
        first_event_timestamp = first_event_series.timestamp
        first_clock_timestamp = self.get_now()


        self.current_event_timestamp = first_event_timestamp
        self.current_clock_timestamp = first_event_timestamp


        # while still_has_rows:
        #     first_event_series = self.df.iloc[0]

        event_series = self.df.iloc[0]
        topic: Topic = event_series.topic
        if topic == "vehicule_changed_status":
            event = series_to_vehicle_event(event_series)
            self.publish(event)
    
    def next(self):
        current_clock_timestamp = self.get_now()
        ellapsed = current_clock_timestamp - self.current_clock_timestamp
        t0 = self.current_event_timestamp
        t1 = 
        self.df.loc[t0:t1]

        

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
