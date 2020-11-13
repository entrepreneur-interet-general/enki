.. backend-reference:

==========
Repository
==========

.. image:: backend/notebook/enki.png

Backend
^^^^^^^

```
docker network create --driver=bridge enki_default
cd auth && docker-compose -f docker-compose.yml up 
```
wait keycloak startup
``` 
docker-compose -f docker-compose.provision.yml run --rm keycloak-provision
cd elk && docker-compose -f docker-compose.yml up 
cd kong && docker-compose -f docker-compose.yml setup 
```
wait kong startup 
```
docker-compose -f docker-compose.provision.yml run --rm kong-provision
cd backend && docker-compose -f docker-compose.yml up
```

FrontEnd
^^^^^^^^

