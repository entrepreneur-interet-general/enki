from cisu.src.constants.constants import WhatsHappenConstants, LocationKindConstants, \
    RiskThreatConstants, HealthMotiveConstants
from cisu.src.entities.commons.common_alerts import WhatsHappen, LocationKind, HealthMotive, RiskThreat


def test_what_happens():
    ch = WhatsHappenConstants()
    all_nature = ch.list_all()
    assert len(all_nature) == 299
    assert isinstance(all_nature[0], WhatsHappen)
    assert [e for e in all_nature if e.code == "C03.07.00"][0].label == "Disparition d'animal"

def test_location_kind():
    ch = LocationKindConstants()
    all_location_kind = ch.list_all()
    assert len(all_location_kind) == 179
    assert isinstance(all_location_kind[0], LocationKind)


def test_risk_threat():
    ch = RiskThreatConstants()
    all_risk_threat = ch.list_all()
    assert len(all_risk_threat) == 37
    assert isinstance(all_risk_threat[0], RiskThreat)


def test_risk_threats():
    ch = HealthMotiveConstants()
    all_health_motive = ch.list_all()
    assert len(all_health_motive) == 52
    assert isinstance(all_health_motive[0], HealthMotive)
