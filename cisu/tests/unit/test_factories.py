from cisu.src.cisu.factories.alert_code_factory import AlertCodeFactory
from cisu.src.cisu.factories.alert_factory import PrimaryAlertFactory
from cisu.src.cisu.factories.edxl_factory import EdxlMessageFactory


def test_alert_factory():
    alert = PrimaryAlertFactory().build()
    alert2 = PrimaryAlertFactory().build()
    assert alert.alertId != alert2.alertId


def test_alert_code_factory():
    alert = AlertCodeFactory().build()
    alert2 = AlertCodeFactory().build()
    assert alert.riskThreat != alert2.riskThreat


def test_edxl_factory():
    edxl = EdxlMessageFactory().build()
    edxl2 = EdxlMessageFactory().build()
    assert edxl.distributionID != edxl2.distributionID
