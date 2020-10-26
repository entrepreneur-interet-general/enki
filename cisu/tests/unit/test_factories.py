from cisu.src.factories.alert_factory import AlertFactory


def test_alert_factory():
    alert = AlertFactory().build()
    alert2 = AlertFactory().build()
    assert alert.alertId != alert2.alertId
