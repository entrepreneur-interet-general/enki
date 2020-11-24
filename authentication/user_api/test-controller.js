var express = require('express');
var router = express.Router();
const keycloak = require('./configuration/keycloak-config.js').getKeycloak();

router.get('/anonymous', function(req, res){
    res.send("Hello Anonymous " + req.headers.authorization.split(' ')[1]);
});
router.get('/user', keycloak.protect('user'), function(req, res){
    res.send("Hello User");
});

router.get('/admin', keycloak.protect('admin'), function(req, res){
    // const userId = jwt_decode(req.headers.authorization.split(' ')[1]).sub
    console.log('ça marche quand même')
    res.send("Hello Admin ");
    
    
});

router.get('/all-user', function(req, res){
    res.send("Hello All User");
});

module.exports = router;