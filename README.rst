==========
Repository
==========

- 1 Backend (shared) : ![backend documentation](/backend/README.rst)
- 3 Front
    * front commandment (dedicated to the firefighter on a daily basis: operational coverage management, simulator, decision support,...)
    * front passive watch (intended for mayors, elected officials, general): high-level watch, alerts)
    * front crisis orchestration : tasks management

# Run keycloak
* `make run` in /auth-enki folder
* Go to localhost:8080
* log in: admin, pwd: Pa55w0rd
* Go to administration console
* Click import & "select file"
* auth-enki/realm-export.json

# Run Enki front
* `nx serve enki` within /fronts folder