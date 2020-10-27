import pathlib
import json

from dataclasses import dataclass
from typing import List

from ..entities.commons.common_alerts import AttributeType, WhatsHappen, LocationKind, \
    RiskThreat, HealthMotive


@dataclass
class ConstantHandler:
    attribute_type_class: AttributeType
    child_keyword: str = "enfants"

    def __init__(self, name: str):
        self.path_constant = pathlib.Path(pathlib.Path(__file__).parent.absolute(), name)

    def data_from_json_file(self) -> list:
        with open(self.path_constant, "r") as f:
            data = json.load(f)
            return data

    def list_all(self) -> List[AttributeType]:
        data: list = self.data_from_json_file()
        has_childs = self.list_has_childs(data)
        while has_childs:
            for e in data:
                childs = e.pop(self.child_keyword, [])
                data.extend(childs)
                has_childs = self.list_has_childs(data)
        return [self.attribute_type_class(**d, comment=None) for d in data]

    def list_has_childs(self, data_list: list) -> bool:
        return any([e.get(self.child_keyword, False) for e in data_list])


class WhatsHappenConstants(ConstantHandler):
    attribute_type_class:WhatsHappen = WhatsHappen

    def __init__(self):
        super(WhatsHappenConstants, self).__init__(name="nature-de-fait.json")


class LocationKindConstants(ConstantHandler):
    attribute_type_class = LocationKind

    def __init__(self):
        super(LocationKindConstants, self).__init__(name="type-de-lieu.json")


class RiskThreatConstants(ConstantHandler):
    attribute_type_class = RiskThreat

    def __init__(self):
        super(RiskThreatConstants, self).__init__(name="risque-menaces.json")


class HealthMotiveConstants(ConstantHandler):
    attribute_type_class = HealthMotive

    def __init__(self):
        super(HealthMotiveConstants, self).__init__(name="pathologies.json")
