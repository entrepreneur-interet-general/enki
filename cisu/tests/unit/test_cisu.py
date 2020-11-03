import pathlib
from datetime import datetime, timezone
from tempfile import NamedTemporaryFile
import xml.dom.minidom

from typing import List, Dict, Any

from cisu.src import EdxlEntity
from cisu.src.entities.alert_entity import PrimaryAlertEntity
from cisu.src.entities.cisu_entity import CreateEvent, Recipient
from cisu.src.entities.commons import Severity
from cisu.src.entities.commons.common_alerts import AnyURI
import xmlschema
import pytest

filenames = list(pathlib.Path(pathlib.Path(__file__).parent.absolute()).glob("data/*.xml"))

expected: Dict[str, Dict[str, Any]] = {
    "4bc6d047-bf3f-439a-93ed-6f18b64eb579.xml": {
        "distributionID": "3d2fec39-bed0-4d74-b198-964aaf19f9ce",
        "receivedAt": datetime(2020, 11, 2, 15, 52, 30, tzinfo=timezone.utc),
        "recipients": [
            Recipient(name='sgc-enki', URI=AnyURI('sge:sgc-enki'))
        ]
    },
    "9a009967-00f6-480c-aa70-78ffe52221fc.xml": {
        "distributionID": "5d7312c3-d631-4608-a4f6-3a4b89961d8d",
        "receivedAt": datetime(2020, 11, 2, 16, 5, 11, tzinfo=timezone.utc),
        "recipients": [
            Recipient(name='police-77', URI=AnyURI('sge:sgo-police-77')),
            Recipient(name='sgc-enki', URI=AnyURI('sge:sgc-enki'))
        ]
    },
    "b785a68f-13b6-4b63-bb41-f7453e267358.xml": {
        "distributionID": "af0d6e0a-39c4-4b96-9f9c-1a06bab2d1b7",
        "receivedAt": datetime(2020, 11, 2, 15, 52, 10, tzinfo=timezone.utc),
        "recipients": [
            Recipient(name='pompiers-77', URI=AnyURI('sge:77-cgo')),
            Recipient(name='sgc-enki', URI=AnyURI('sge:sgc-enki'))
        ]
    },
    "b6650872-42f6-4bb5-ace5-760d005632b5.xml": {
        "distributionID": "443dbab3-7106-42f6-80c6-5f698c74215b",
        "receivedAt": datetime(2020, 11, 2, 15, 52, 52, tzinfo=timezone.utc),
        "recipients": [
            Recipient(name='pompiers-91', URI=AnyURI('sge:91-cgo')),
            Recipient(name='sgc-enki', URI=AnyURI('sge:sgc-enki'))
        ]
    },
    "edxl-de-affaire.test.xml": {
        "distributionID": "21b36a36-717b-4eba-bbc1-8e027624fe2f",
        "receivedAt": datetime(2020, 4, 6, 12, 2, 0, tzinfo=timezone.utc),
        "recipients": [
            Recipient(name='pompier-sdis77', URI=AnyURI('sge:pompier-sdis77')),
            Recipient(name='police-77', URI=AnyURI('sge:sgo-police-77'))
        ]
    }
}


@pytest.mark.parametrize("filename", filenames)
def test_edxl_xml_parsing(filename):
    print(filename)
    suffix = str(filename).split("/")[-1]
    dom = xml.dom.minidom.parse(str(filename))
    edxl = EdxlEntity.from_xml(dom)
    assert edxl.distributionID == expected[suffix]["distributionID"]
    assert isinstance(edxl.resource.message.choice, CreateEvent)
    assert edxl.resource.message.choice.primaryAlert.receivedAt.value == expected[suffix]["receivedAt"]
    assert isinstance(edxl.resource.message.choice.primaryAlert, PrimaryAlertEntity)

    assert isinstance(edxl.resource.message.choice.primaryAlert.resource, list)
    assert edxl.resource.message.recipients == expected[suffix]["recipients"]
    assert edxl.resource.message.choice.severity == Severity.SEVERE

@pytest.mark.parametrize("filename", filenames)
def test_edxl_xml_generation(filename):
    schema_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(), "../../src/entities/schema/cisu.xsd")
    dom = xml.dom.minidom.parse(str(filename))
    edxl = EdxlEntity.from_xml(dom)
    xml_string = edxl.resource.message.to_xml()
    temp_file = NamedTemporaryFile(mode="w", suffix=".xml")
    with open(temp_file.name, "w") as f:
        f.write(xml_string)
    my_schema = xmlschema.XMLSchema(str(schema_path))
    print(my_schema.validate(temp_file.name))
    assert my_schema.is_valid(temp_file.name)
    temp_file.close()
