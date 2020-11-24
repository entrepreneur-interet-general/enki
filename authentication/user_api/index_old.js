const express = require('express')
const app = express()
const fetch = require('node-fetch')
const port = 4201
const jwt_decode = require('jwt-decode')
const jwt = require('jsonwebtoken')
// const Keycloak = require('keycloak-connect');
// const { response } = require('express');
// const KcAdminClient = require('keycloak-admin').default;

const KEYCLOAK_URL= `http://localhost:8084/auth`
const KEYCLOAK_REALM = `enki`
const KEYCLOAK_CLIENT_ID = `admin`
const KEYCLOAK_CLIENT_SECRET= `Pa55w0rd`
const USER_ID = `admin-cli`
const KEYCLOAK_TOKEN_URL = `http://localhost:8084/auth/realms/master/protocol/openid-connect/token`

const tokenKey = `MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmAFlVuj3/HHlnPfDSFRogBeLPngb0s2N9Hv4iC6t999+Ee4FbRfCrjfibhCro8mVK6DS37NRk01PhnMbDakob8hF+XspdeYnOVPVkmkKBbAIv+xm4hbH38DCwifRxjDdF3+Z9F7YOg17sIpi0FQUVeuYp/jcCL2UYtIXGs89gVfhaZPMzZtY0Q681daOHcIzihh8Wy3E0geXhdEmOawbhEJDXgnK3337/CfJJUD0kdvsjilV8jocgotR0yNVriE9ZVKR2LV+2BwFvI3CJmwfRoIoK3OyABI3plpbO4qgHHJisGtOGVDs7AUp6mLYGWjLHE3uuopF0pvUca8mfEd2zQIDAQAB`

const data = {
  "grant_type": "password",
  "username": KEYCLOAK_CLIENT_ID,
  "password": KEYCLOAK_CLIENT_SECRET,
  "client_id": "admin-cli"
};
var formBody = [];
for (var property in data) {
  var encodedKey = encodeURIComponent(property);
  var encodedValue = encodeURIComponent(data[property]);
  formBody.push(encodedKey + "=" + encodedValue);
}
formBody = formBody.join("&");



app.get('/', (req, res) => {

  jwt.verify(req.headers.authorization.split(' ')[1], tokenKey)
  const userId = jwt_decode(req.headers.authorization.split(' ')[1]).sub


  fetch(KEYCLOAK_TOKEN_URL, {
    method: 'POST',
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formBody
  }).then((response) => response.json())
  .then((data) => {
    console.log(userId)
    fetch(`http://localhost:8084/auth/admin/realms/enki/users/${userId}`, {
      headers: {
        "Authorization": `Bearer ${data.access_token}`,
        "method": 'GET',
        "Content-Type": "application/json"
      }
    }).then(response => response.json())
      .then((response) => {
        res.json(response)
      })
  })
 
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

app.put('api/users', (req, res) => {

  /*   console.log(req)
  
    fetch(KEYCLOAK_TOKEN_URL, {
      method: 'POST',
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formBody
    }).then((response) => response.json())
    .then((data) => { */
      fetch(`${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users`, {
        headers: {
          "Authorization": `Bearer ${data.access_token}`,
          "method": 'PUT',
          "Content-Type": "application/json"
        }
      }).then(response => response.json())
        .then((response) => {
          res.json(response)
        })
  /*   }) */
  })