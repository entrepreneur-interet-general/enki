import pathlib
from datetime import datetime, timezone
from tempfile import NamedTemporaryFile
import xml.dom.minidom

from cisu.src import EdxlEntity
from cisu.src.entities.alert_entity import PrimaryAlertEntity
from cisu.src.entities.cisu_entity import CreateEvent, Recipient
from cisu.src.entities.commons import Severity
from cisu.src.entities.commons.common_alerts import AnyURI


def test_edxl_xml_parsing():
    xml_fname = "./edxl-de-affaire.test.xml"
    xml_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(), xml_fname)

    dom = xml.dom.minidom.parse(str(xml_path))
    edxl = EdxlEntity.from_xml(dom)
    assert edxl.distributionID == '21b36a36-717b-4eba-bbc1-8e027624fe2f'
    assert isinstance(edxl.resource.message.choice, CreateEvent)
    assert edxl.resource.message.choice.primaryAlert.receivedAt.value == datetime(2020, 4, 6, 12, 2, tzinfo=timezone.utc)
    assert isinstance(edxl.resource.message.choice.primaryAlert, PrimaryAlertEntity)

    assert isinstance(edxl.resource.message.choice.primaryAlert.resource, list)
    assert edxl.resource.message.recipients == [
        Recipient(name='pompier-sdis77', URI=AnyURI('echanges:pompier-sdis77')),
        Recipient(name='police-77', URI=AnyURI('echanges:sgo-police-77'))
    ]
    assert edxl.resource.message.choice.severity == Severity.SEVERE


def test_edxl_xml_generation():
    import xmlschema

    xml_fname = "./edxl-de-affaire.test.xml"
    xml_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(), xml_fname)
    schema_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(), "../../src/entities/schema/cisu.xsd")
    dom = xml.dom.minidom.parse(str(xml_path))
    edxl = EdxlEntity.from_xml(dom)
    xml_string = edxl.resource.message.to_xml()
    temp_file = NamedTemporaryFile(mode="w", suffix=".xml")
    with open(temp_file.name, "w") as f:
        f.write(xml_string)
    my_schema = xmlschema.XMLSchema(str(schema_path))
    assert my_schema.is_valid(temp_file.name)
    temp_file.close()
