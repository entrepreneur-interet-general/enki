def test_elastic_ping(es_client):
    assert es_client.ping()
