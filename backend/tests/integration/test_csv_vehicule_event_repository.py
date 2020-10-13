from dataclasses import asdict
import pytest
import os

import pandas as pd

from adapters.csv.csv_vehicule_event_repository import CsvVehiculeEventRepository
from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData 
from domain.couv_ops.ports.vehicule_event_repository import AlreadyExistingVehiculeEventUuid
from tests.factories.vehicule_event_factory import make_vehicule_event_entity
from tests.factories import vehicule_event_factory

csv_path = 'tests/integration/temp_data/vehicule_event_entity.csv'
def reset_csv():
    if os.path.exists(csv_path):
        os.remove(csv_path)

def test_can_add_to_csv_vehicule_event_repository():
    reset_csv()
    csv_vehicule_event_repository = CsvVehiculeEventRepository(csv_path=csv_path)
    vehicule_event_entity = make_vehicule_event_entity()
    csv_vehicule_event_repository.add(vehicule_event_entity)
    df = pd.read_csv(csv_path)
    last_row = df.iloc[-1]
    assert not last_row.empty
    assert last_row.uuid == vehicule_event_entity.uuid
    assert pd.Timestamp(last_row.timestamp) == vehicule_event_entity.timestamp
    last_row_values = set(last_row.values)
    vehicule_event_entity_data_values = set(asdict(vehicule_event_entity.data).values())
    assert vehicule_event_entity_data_values.issubset(last_row_values)

def test_cannot_add_to_csv_if_already_exists():
    reset_csv()
    csv_vehicule_event_repository = CsvVehiculeEventRepository(csv_path=csv_path)
    vehicule_event_entity = make_vehicule_event_entity()
    
    with pytest.raises(AlreadyExistingVehiculeEventUuid):
        # add the same event two times
        csv_vehicule_event_repository.add(vehicule_event_entity)
        csv_vehicule_event_repository.add(vehicule_event_entity)