var express = require('express');
var router = express.Router();
var fetch = require('node-fetch');
var jwt_decode = require('jwt-decode');
const keycloak = require('./configuration/keycloak-config.js').getKeycloak();

router.get('/anonymous', function(req, res){
  res.send("Hello Anonymous " + req.headers.authorization.split(' ')[1]);
  
});
router.get('/user', keycloak.protect('realm:user'), function(req, res){
  const userId = jwt_decode(req.headers.authorization.split(' ')[1]).sub
  // res.send("Hello User " + userId);
  // console.log(keyloack.get)
  fetch(`http://localhost:8084/auth/admin/realms/enki/users/${userId}`, {
    method: 'GET',
    headers: {
      "Authorization": `Bearer ${req.headers.authorization.split(' ')[1]}`,
      "Content-Type": "application/json"
    }
  })
  .then(response => response.json())
  .then((response) => {
    res.json(response)
  })
  .catch((error) => {
    console.error(error)
  })
});


router.put('/user', keycloak.protect('realm:user'), function(req, res) {
  const userId = jwt_decode(req.headers.authorization.split(' ')[1]).sub;
  // console.log('blalsndf ' + req.body.firstName)
  console.log(`http://localhost:8084/auth/admin/realms/enki/users/${userId}`)
  fetch(`http://localhost:8084/auth/admin/realms/enki/users/${userId}`, {
    method: 'PUT',
    headers: {
      "Authorization": `Bearer ${req.headers.authorization.split(' ')[1]}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(req.body)
  })
  .then((response) => {
    res.json(response)
  })
  .catch((error) => {
    console.error(error)
  })

  fetch(`http://localhost:8084/auth/admin/realms/enki/users/${userId}/groups/ac11e7e5-6a05-481d-8966-a19de5bdbd15`, {
    method: 'PUT',
    headers: {
      "Authorization": `Bearer ${req.headers.authorization.split(' ')[1]}`,
      "Content-Type": "application/json"
    }
  })
  .then(response => response.json())
  .then((response) => {
    res.json(response)
  })
  .catch((error) => {
    console.error(error)
  })
})
/* 
router.post('/user', keycloak.protect('realm:user'), function(req, res) {
  fetch(`http://localhost:8084/auth/admin/realms/enki/users/${userId}`, {
  headers: {
    "Authorization": `Bearer ${req.headers.authorization.split(' ')[1]}`,
    "method": 'PUT',
    "Content-Type": "application/json"
  },
  body: formBody
}).then(response => response.json())
.then((response) => {
  res.json(response)
})
}) */
router.get('/testRoute', keycloak.protect(), function(req, res){
  // const userId = jwt_decode(req.headers.authorization.split(' ')[1]).sub
  console.log('ça marche quand même')
  res.send("Hello Admin ");
});

router.get('/admin', keycloak.protect('realm:app-admin'), function(req, res){
  // const userId = jwt_decode(req.headers.authorization.split(' ')[1]).sub
  console.log('ça marche quand même')
  res.send("Hello Admin ");
});

router.get('/all-user', function(req, res){
  res.send("Hello All User");
});

module.exports = router;