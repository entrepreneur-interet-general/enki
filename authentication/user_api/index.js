var express = require('express');
var app = express();
var cors = require('cors');
var bodyParser = require('body-parser');

app.use(cors());
app.use(bodyParser());

const keycloak = require('./configuration/keycloak-config.js').initKeycloak();
app.use(keycloak.middleware());

var controller = require('./controller/controller.js');
app.use('/api', controller);

app.get('/', function(req, res){
   res.send("Server is up!");
});

app.listen(4201);