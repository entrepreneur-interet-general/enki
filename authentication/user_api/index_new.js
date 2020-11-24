// Nous importons Express dans notre application
import express from 'express';
import bodyParser from 'body-parser';
import session from 'express-session';
import Keycloak from 'keycloak-connect';

// Notre Application utilisera express grace à cette ligne
const app = express();
app.use(bodyParser.json());

const memoryStore = new session.MemoryStore();
app.use(
  session({
    secret: 'secretKey',
    resave: false,
    saveUninitialized: true,
    store: memoryStore
  })
);
const keycloak = new Keycloak({
  store: memoryStore
});
app.use(
  keycloak.middleware({
    logout: '/logout',
    admin: '/'
  })
);
// Voici notre 1ere route
app.get('/api/unsecured', function(req, res) {
  res.send('Welcome to home page');
});

app.get('/api/user', keycloak.protect('realm:user'), function(req, res) {
  res.json({ message: 'This is an USER endpoint payload' });
});

app.get('/api/admin', keycloak.protect('realm:admin'), function(req, res) {
  res.json({ message: 'This is an ADMIN endpoint payload' });
});

// Si tout se passe bien notre application écoutera sur le port 3000
app.listen(3000, err => {
  if (err) {
    console.error(err);
  }
  {
    console.log(`APP Listen to port : 3000`);
  }
});