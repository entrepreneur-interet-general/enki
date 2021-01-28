import requests
import os
# from dotenv import load_dotenv
# load_dotenv("../../.env")

KONG_HOST_IP = os.environ.get("KONG_HOST_IP")
KONG_PORT = os.environ.get("KONG_PORT")
KEYCLOAK_HOST_IP = os.environ.get("KEYCLOAK_HOST_IP")
KEYCLOAK_PORT = os.environ.get("KEYCLOAK_PORT")

BACKEND_URI = os.environ.get("BACKEND_URI")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

ENKI_API_SERVICE_ID = os.environ.get("ENKI_API_SERVICE_ID")

data = [
  ('name', 'cors'),
  ('config.origins', 'http://localhost:1337/*'),
  ('config.methods', 'GET'),
  ('config.methods', 'POST'),
  ('config.methods', 'OPTIONS'),
  ('config.methods', 'PUT'),
  ('config.methods', 'DELETE'),
  ('config.headers', 'Accept'),
  ('config.headers', 'Accept-Version'),
  ('config.headers', 'Content-Length'),
  ('config.headers', 'Content-MD5'),
  ('config.headers', 'Content-Type'),
  ('config.headers', 'Authorization'),
  ('config.headers', 'Date'),
  ('config.headers', 'X-Auth-Token'),
  ('config.exposed_headers', 'X-Auth-Token'),
  ('config.credentials', 'true'),
  ('config.max_age', '3600')
]

response = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services/%3Cservice%3E/plugins', data=data)
