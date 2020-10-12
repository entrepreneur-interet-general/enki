from dataclasses import asdict
from tests.factories.vehicule_event_factory import make_vehicule_event_entity
from tests.factories import vehicule_event_factory
import pandas as pd
import os
from adapters.csv.csv_vehicule_event_repository import CsvVehiculeEventRepository

from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData 

def test_csv_vehicule_event_repository():
    df_vehicule_event = pd.DataFrame()
    csv_path = 'tests/integration/temp_data/vehicule_event_entity.csv'
    if os.path.exists(csv_path):
        os.remove(csv_path)
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

