from cisu.src.factories.alert_code_factory import AlertCodeFactory
from cisu.src.factories.alert_factory import AlertFactory


def test_alert_factory():
    alert = AlertFactory().build()
    alert2 = AlertFactory().build()
    assert alert.alertId != alert2.alertId


def test_alert_code_factory():
    alert = AlertCodeFactory().build()
    alert2 = AlertCodeFactory().build()
    assert alert.riskThreat != alert2.riskThreat
