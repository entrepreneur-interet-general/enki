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

# Add Service for enki URL
data = {
    'name': 'enki_api',
    'url': f'{BACKEND_URI}'
}
print(f'http://{KONG_HOST_IP}:{KONG_PORT}/services')
print(data)

response = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services', data=data)

print(response.json())

created_service_id = response.json()["id"]

# # Add routes path


data = {
    'service.id': f'{created_service_id}',
    'paths[]': '/enki',
}

_ = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services/enki_api/routes', data=data)

# # Configure OIDC Plugin


data = {
    'name': 'oidc',
    'config.client_id': f'{CLIENT_ID}',
    'config.client_secret': f'{CLIENT_SECRET}',
    'config.discovery': f'http://{KEYCLOAK_HOST_IP}:{KEYCLOAK_PORT}/auth/realms/enki/.well-known/openid-configuration'
}

_ = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/plugins', data=data)
