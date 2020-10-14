from datetime import datetime, timedelta
from typing import List

import pytest
from domain.couv_ops.ports.event_bus import Event
from heplers.now import CustomNow
from tests.integration.csv_test_helpers import reset_csv
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

from adapters.csv.csv_helpers import event_to_series
from tests.factories.vehicule_event_factory import make_vehicule_event
from adapters.csv.csv_scheduled_event_bus import CsvError, CsvScheduledEventBus

csv_path = 'tests/integration/temp_data/events_to_dispatch.csv'

def create_csv_events_to_dispatch(path: str):
    reset_csv(path)
    timestamps = [pd.Timestamp("2020-10-01T12:01"), pd.Timestamp("2020-10-01T12:01:03"), pd.Timestamp("2020-10-01T12:00")]

    list_series = []
    for timestamp in timestamps:
        event = make_vehicule_event(timestamp=timestamp)
        list_series.append(event_to_series(event))

    df = pd.DataFrame(list_series)
    df.to_csv(path)
    return df

now = CustomNow()

def test_fails_if_csv_not_found():
    with pytest.raises(CsvError) as e:
        CsvScheduledEventBus(now, csv_path="notfound/file.csv")
    assert str(e.value) == "Csv_path or DF should be provided"

    with pytest.raises(CsvError) as e2:
        CsvScheduledEventBus(now, )
    assert str(e2.value) == "Csv_path or DF should be provided"

def test_fails_if_csv_format_is_incorrect():
    df = create_csv_events_to_dispatch(csv_path)
    missing_col_df = df.drop('timestamp', axis=1)
    with pytest.raises(CsvError) as e3:
        CsvScheduledEventBus(now, df=missing_col_df)
    assert str(e3.value) == "Some columns are missing : {'timestamp'}"
    
    timestamp_as_str_df = df.copy()
    timestamp_as_str_df.timestamp = timestamp_as_str_df.timestamp.astype(str)
    event_bus = CsvScheduledEventBus(now, df=timestamp_as_str_df)
    assert is_datetime(event_bus.df.timestamp)
    assert event_bus.df.timestamp.is_monotonic

    timestamp_with_wrong_str_df = timestamp_as_str_df.copy()
    timestamp_with_wrong_str_df.timestamp[0] = "wrong"
    with pytest.raises(CsvError) as e4:
        CsvScheduledEventBus(now, df=timestamp_with_wrong_str_df)
    assert str(e4.value) == "Timestamp cannot be converted to datetime"

    


def test_provided_event_get_dispatched_correctly():
    published_events: List[Event] = []
    df = create_csv_events_to_dispatch(csv_path)

    test_start_time = datetime.strptime("2020-10-02 15:00", "%Y-%m-%d %H:%M")
    now.set_next_date(test_start_time)

    event_bus = CsvScheduledEventBus(now, df=df)
    
    spy = lambda event: published_events.append(event)
    event_bus.subscribe("vehicule_changed_status", spy)
    event_bus.start(time_step=10)

    assert published_events[0].uuid == df.uuid.iloc[0]

    test_plus_1_min = test_start_time + timedelta(minutes=1)
    now.set_next_date(test_plus_1_min)
    assert len(published_events) == 1

    test_plus_1_min_30_s = test_plus_1_min + timedelta(seconds=30)
    now.set_next_date(test_plus_1_min_30_s)
    assert len(published_events) == 3
