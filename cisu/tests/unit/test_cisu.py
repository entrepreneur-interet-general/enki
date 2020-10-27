import pathlib
from datetime import datetime, timezone
from cisu.src import EdxlEntity
from cisu.src.entities.alert_entity import PrimaryAlertEntity
from cisu.src.entities.cisu_entity import CreateEvent, Recipient
from cisu.src.entities.commons import Severity
from cisu.src.entities.commons.common_alerts import AnyURI


def test_edxl_xml_parsing():
    import xml.dom.minidom
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
        Recipient(name='pompier-sdis77', URI=AnyURI('sge:pompier-sdis77')),
        Recipient(name='police-77', URI=AnyURI('sge:sgo-police-77'))
    ]
    assert edxl.resource.message.choice.severity == Severity.SEVERE
