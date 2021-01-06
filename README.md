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
```
cd authentication
```
Copy example.env to .env 
```
cp example.env .env
``` 
Change variables if needed

```
 docker-compose -f docker-compose.yml up 
```
wait keycloak startup
``` 
docker-compose -f docker-compose.provision.yml run --rm keycloak-provision
```

or with make 
```
make upd && sleep 5 && make provision 
```

````
cd user_api
````
Run the user api
```
npm start
````
It is now accessible on http://localhost:4201/api


Get kong client secret from Keycloak admin in Client section and change it in .env file
### Kong Api Gateway

```
cd kong
```
Copy example.env to .env 
```
cp example.env .env
``` 
Change CLIENT_SECRET with keycloak kong client

``` 
docker-compose -f docker-compose.yml setup 
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
cd elk
```
```
docker-compose -f docker-compose.yml up
```
or with make 
```
make upd
```
### Backend
```
cd backend
```

```
docker-compose -f docker-compose.yml up
```
or with make 
```
make upd 
```

It's now possible to post new "affaires" in postman with this endpoint:

```
http://localhost:5000/api/v1/echanges/messages
```

You can access affairs from:
```
http://localhost:5000/api/enki/v1/affairs?code_insee=77108
```
You also have to start SIG in nexsis/sig/api
```
make install
npm run seed
make start
```

### FrontEnd
```
cd front
```

```
yarn
```

and run angular
```
ng serve 
```

Go to http://localhost:1337
You can login with:
Login: maire@chelles.fr
PWD: defaultpassword


### Design system
````
cd design-system
````

Develop
```
make up
````

Deploy to heroku
Merge all design-system modifications to `main` branch
and run
```
make deploy
```
(you have to be logged in to heroku to have access, and ask admin a collab access)
