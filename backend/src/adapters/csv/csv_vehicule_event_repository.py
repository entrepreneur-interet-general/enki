from dataclasses import Field, asdict, field, fields
import pathlib
from typing import Dict, List, Union
import pandas as pd 
import os

from pandas.core.indexes.datetimes import DatetimeIndex 

from domain.couv_ops.ports.vehicule_event_repository import AbstractVehiculeEventRepository
from domain.couv_ops.entities.vehicule_event_entity import VehiculeEventEntity
from domain.couv_ops.value_objects.vehicule_event_data import VehiculeEventData

class CsvVehiculeEventRepository(AbstractVehiculeEventRepository):
    def __init__(self, csv_path: str = 'data/vehicule_event_entity.csv'):
        self.csv_path = csv_path
        event_fields = [field for field in fields(VehiculeEventEntity) if field.name != 'data']
        data_fields = list(fields(VehiculeEventData))
        columns_fields = event_fields + data_fields
        
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        series = self._create_series_from_fields(columns_fields)
        self.df = pd.DataFrame(series)
        self._save()

    def _save(self):
        self.df.to_csv(self.csv_path, index=False)
        
    def _add(self, vehicule_event_entity : VehiculeEventEntity) -> None:

        data_dict = asdict(vehicule_event_entity.data)
        flatten_row = asdict(vehicule_event_entity)
        del flatten_row['data']
        flatten_row.update(data_dict)
        self.df = self.df.append(pd.Series(flatten_row), ignore_index=True)
        self._save()

    def _match_uuid(self, uuid: str) -> Union[VehiculeEventEntity, None]:
        _matches = self.df[self.df.uuid == uuid]
        return self._series_to_entity(_matches.iloc[0]) if not _matches.empty else None

    @staticmethod
    def _create_series_from_fields(fields: List[Field]) -> Dict[str, pd.Series]:
        series = {}
        for field in fields: 
            dtype = field.type.__name__ if hasattr(field.type, '__name__') else 'str'
            if dtype == 'Timestamp': 
                dtype = 'datetime64[ns]'
            series[field.name] = pd.Series([], dtype=dtype)
        return series

    @staticmethod
    def _series_to_entity(series: pd.Series) -> VehiculeEventEntity:
        isin_timestamp_uuid = series.index.isin(['timestamp', 'uuid'])

        series_timestamp_uuid = series[isin_timestamp_uuid].to_dict()
        series_data = series[~isin_timestamp_uuid].to_dict()

        data = VehiculeEventData(**series_data)
        entity = VehiculeEventEntity(data=data, **series_timestamp_uuid)
        return entity
