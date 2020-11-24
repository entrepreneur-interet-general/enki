var session = require('express-session');
var Keycloak = require('keycloak-connect');

let _keycloak;

var keycloakConfig = {
    "realm": "enki",
    "bearer-only": true,
    "auth-server-url": "http://localhost:8084/auth/",
    "ssl-required": "external",
    "resource": "api-nodejs",
    "verify-token-audience": true,
    "use-resource-role-mappings": true,
    "confidential-port": 0,
    "credentials": {
        "clientSecret": "06783024-faa8-450b-b94d-9c25c64bf697"
    }
};

function initKeycloak() {
    if (_keycloak) {
        console.warn("Trying to init Keycloak again!");
        return _keycloak;
    } 
    else {
        console.log("Initializing Keycloak...");
        var memoryStore = new session.MemoryStore();
        _keycloak = new Keycloak({ store: memoryStore }, keycloakConfig);
        return _keycloak;
    }
}

function getKeycloak() {
    if (!_keycloak){
        console.error('Keycloak has not been initialized. Please called init first.');
    } 
    return _keycloak;
}

module.exports = {
    initKeycloak,
    getKeycloak
};