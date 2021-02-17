# End-to-end tests for Enki

## Before running tests

### Make sure you have everything clean

* Backend: `make down && make upd && make sleep 5 && make seed`
* Frontend: `ng serve`
* Keycloak: Remove users mairie@chelles.fr and prefet@seineetmarne.fr if they already exist (from localhost:8080), if you re-run it, make sure you change Kong client secret in the Kong .env file
* Kong: Run it


## Run tests

### Test registration

Description: Will try to create mairie@chelles.fr and prefet@seineetmarne.fr users

```
testcafe chrome register.js
```

---

### Test login and all _événements_ related features

Description: Will try
* login as mairie@chelles.fr
* create an event
* add a message with a label and a resource

```
testcafe chrome testAsMaire.js
```
