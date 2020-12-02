var express = require('express');
var router = express.Router();
var fetch = require('node-fetch');
var jwt_decode = require('jwt-decode');
const keycloak = require('../configuration/keycloak-config.js').getKeycloak();


const KEYCLOAK_URL = `http://localhost:8084/auth`;
const KEYCLOAK_REALM = `enki`;
const KEYCLOAK_USERS_ENDPOINT = `${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users`;
const KEYCLOAK_GROUPS_ENDPOINT = `${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/groups`;

router.get('/anonymous', function(req, res){
  res.send("Hello Anonymous " + req.headers.authorization.split(' ')[1]);
  
});
router.get('/user', keycloak.protect('realm:user'), function(req, res){
  const userId = jwt_decode(req.headers.authorization.split(' ')[1]).sub
  fetch(`${KEYCLOAK_USERS_ENDPOINT}/${userId}`, {
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
  // throw new Error('BROKEN')
  const bearerToken = req.headers.authorization.split(' ')[1]
  const userId = jwt_decode(bearerToken).sub;
  const headers = {
    "Authorization": `Bearer ${bearerToken}`,
    "Content-Type": "application/json"
  }

  console.log(`${KEYCLOAK_USERS_ENDPOINT}/${userId}`)
  
  // the user is updated with user representation given in body
  fetch(`${KEYCLOAK_USERS_ENDPOINT}/${userId}`, {
    method: 'PUT',
    headers: headers,
    body: JSON.stringify({
      attributes: {
        "communes": req.body.attributes.communes,
        "fonction": req.body.attributes.fonction
      },
      firstName: req.body.firstName,
      lastName: req.body.lastName
    })
  })
  // .then(response => response.json())
  .then(response => {

    // we had directly without verifying the user to the group being user_fonction
    if (req.body.user_fonction) {
      // fetch all the existing groups
      fetch(`${KEYCLOAK_GROUPS_ENDPOINT}`, {
        method: 'GET',
        headers: headers
      })
      .then((response) => response.json())
      .then((groupArr) => {
        const groupId = groupArr.filter(group => {
          return group.name === req.body.user_fonction ? true : false
        })[0].id;
    
        // and apply group on user depending on what qwas sent in body
        fetch(`${KEYCLOAK_USERS_ENDPOINT}/${userId}/groups/${groupId}`, {
          method: 'PUT',
          headers: headers
        })
        .then((response) => {
          res.send(response)
        })
        .catch((error) => {
          console.error(error)
        })
      }).catch((error) => {
        console.error("Error when trying to fetch groups: " + error)
      })
    } else {
      res.json(response)
    }
  }).catch(error => {
    console.error('Error while fetching update user: ' + error)
  })



})

router.get('/admin', keycloak.protect('realm:app-admin'), function(req, res){
  res.send("Hello Admin ");
});


module.exports = router;