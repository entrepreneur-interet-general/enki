import asyncio
from datetime import datetime
import logging
import pytest
from typing import List

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

from adapters.csv.csv_helpers import event_to_series
from adapters.csv.csv_scheduled_event_bus import CsvError, CsvScheduledEventBus
from domain.couv_ops.ports.event_bus import Event, Topic
from heplers.clock import CustomClock
from tests.integration.csv_test_helpers import reset_csv
from tests.factories.vehicule_event_factory import make_vehicule_event


csv_path = 'tests/integration/temp_data/events_to_dispatch.csv'

def create_csv_events_to_dispatch(path: str):
    reset_csv(path)
    timestamps = [
        pd.Timestamp("2020-10-01T12:01"), 
        pd.Timestamp("2020-10-01T12:01:03"), 
        pd.Timestamp("2020-10-01T12:00")]

    list_series = []
    for timestamp in timestamps:
        event = make_vehicule_event(timestamp=timestamp)
        list_series.append(event_to_series(event))

    df = pd.DataFrame(list_series)
    df.to_csv(path)
    return df

clock = CustomClock()

def test_fails_if_csv_not_found():
    with pytest.raises(CsvError) as e:
        CsvScheduledEventBus(clock, csv_path="notfound/file.csv")
    assert str(e.value) == "Csv_path or DF should be provided"

    with pytest.raises(CsvError) as e2:
        CsvScheduledEventBus(clock)
    assert str(e2.value) == "Csv_path or DF should be provided"

def test_fails_if_csv_format_is_incorrect():
    df = create_csv_events_to_dispatch(csv_path)
    missing_col_df = df.drop('timestamp', axis=1)
    with pytest.raises(CsvError) as e3:
        CsvScheduledEventBus(clock, df=missing_col_df)
    assert str(e3.value) == "Some columns are missing : {'timestamp'}"
    
    timestamp_as_str_df = df.copy()
    timestamp_as_str_df.timestamp = timestamp_as_str_df.timestamp.astype(str)
    event_bus = CsvScheduledEventBus(clock, df=timestamp_as_str_df.copy())
    assert is_datetime(event_bus.df.timestamp)
    assert event_bus.df.timestamp.is_monotonic

    timestamp_with_wrong_str_df = timestamp_as_str_df
    timestamp_with_wrong_str_df.timestamp[0] = "wrong"
    with pytest.raises(CsvError) as e4:
        CsvScheduledEventBus(clock, df=timestamp_with_wrong_str_df)
    assert str(e4.value) == "Timestamp cannot be converted to datetime"

    
test_start_time = datetime.strptime("2020-10-02 15:00", "%Y-%m-%d %H:%M")
def prepare_event_bus_and_spy(resync):
    published_events: List[Event] = []
    df = create_csv_events_to_dispatch(csv_path)
    clock.set_next_date(test_start_time)

    event_bus = CsvScheduledEventBus(clock,  df=df)
    
    spy = lambda event: published_events.append(event)
    event_bus.subscribe("vehicule_changed_status", spy)
    event_bus.start(resync=resync)
    return event_bus, published_events

async def _async_test_one_step(event_bus,  speed, time_step, published_events, expected_dispatched_events_timestamps):
    # dispatch first event 
    clock = event_bus.clock
    awaken_event = asyncio.Event()
    looping_task = asyncio.create_task(event_bus._async_loop(time_step, speed))
    clock.set_awaken_event(awaken_event)
    await clock.wake_up()
    await looping_task
    assert [event.timestamp for event in published_events] == expected_dispatched_events_timestamps

def test_provided_event_get_dispatched_correctly():
    speed = 1
    time_step = 1
    resync = False

    event_bus, published_events = prepare_event_bus_and_spy(resync)

    expected_dispatched_events_timestamps = [pd.Timestamp('2020-10-01 12:00:00')]
    asyncio.run(_async_test_one_step(event_bus, speed, time_step, published_events, expected_dispatched_events_timestamps))
    
    # Adding 5 seconds and call next.
    clock.add_seconds(5)
    _async_test_one_step(event_bus, speed, time_step, published_events, expected_dispatched_events_timestamps)

    # Adding 60 seconds and call next
    clock.add_seconds(60)
    expected_dispatched_events_timestamps =  [pd.Timestamp('2020-10-01 12:00:00'), pd.Timestamp("2020-10-01T12:01"), pd.Timestamp("2020-10-01T12:01:03")]
    _async_test_one_step(event_bus, speed, time_step, published_events, expected_dispatched_events_timestamps)

def test_streaming_speed():
    speed = 60 
    time_step = 1 
    resync = False

    event_bus, published_events = prepare_event_bus_and_spy(resync)
    
    clock.add_seconds(1) # equivalent to 60 seconds 

    expected_dispatched_events_timestamps =  [pd.Timestamp('2020-10-01 12:00:00'), pd.Timestamp("2020-10-01T12:01")]
    _async_test_one_step(event_bus, speed, time_step, published_events, expected_dispatched_events_timestamps)

def test_resync():
    speed = 1
    time_step = 1 
    resync = True

    event_bus, published_events = prepare_event_bus_and_spy(resync)
    clock.add_seconds(1) 
    expected_dispatched_events_timestamps =  [pd.Timestamp(test_start_time)]
    _async_test_one_step(event_bus, speed, time_step, published_events, expected_dispatched_events_timestamps)


