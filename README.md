.. image:: backend/notebook/enki.png

## Installation

This is a little trick to redirect to keycloak from localhost 
```
echo "localhost keycloak" >> /etc/hosts
```
or add it manually with your bests text editor 

You need to create global default network with 
```
docker network create --driver=bridge enki_default
``` 

### Keycloak
Copy example.env to .env 
```
cp example.env .env
``` 
Change variables if needed

```
cd auth && docker-compose -f docker-compose.yml up 
```
wait keycloak startup
``` 
docker-compose -f docker-compose.provision.yml run --rm keycloak-provision
```

or with make 
```
make upd && sleep 5 && make provision 
```

Get kong client secret from Keycloak admin in Client section and change it in .env file
### Kong Api Gateway
Copy example.env to .env 
```
cp example.env .env
``` 
Change CLIENT_SECRET with keycloak kong client

``` 
cd kong && docker-compose -f docker-compose.yml setup 
```
wait kong startup 
```
docker-compose -f docker-compose.provision.yml run --rm kong-provision
```

or with make 
```
make setup && sleep 5 && make provision 
```
# Elasticsearch and Kibana
```
cd elk && docker-compose -f docker-compose.yml up
```
or with make 
```
make upd
```
### Backend

```
cd backend && docker-compose -f docker-compose.yml up
```
or with make 
```
make upd 
```
### FrontEnd
```
cd front && docker-compose -f docker-compose.yml up
```
or with make 
```
make upd 
```

