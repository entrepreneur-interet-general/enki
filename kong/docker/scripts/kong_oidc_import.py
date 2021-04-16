import requests
import os

# from dotenv import load_dotenv
# load_dotenv("../../.env")

KONG_HOST_IP = os.environ.get("KONG_HOST_IP")
KONG_PORT = os.environ.get("KONG_PORT")
KEYCLOAK_HOST_IP = os.environ.get("KEYCLOAK_HOST_IP")
KEYCLOAK_PORT = os.environ.get("KEYCLOAK_PORT")
IS_PROD = os.environ.get("PROD") == "true"

BACKEND_URI = os.environ.get("BACKEND_URI")
FRONTEND_URI = os.environ.get("FRONTEND_URI")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REALM_NAME = "enki"

ENKI_BACKEND_SERVICE_ID = os.environ.get("ENKI_BACKEND_SERVICE_ID")
ENKI_FRONT_SERVICE_ID = os.environ.get("ENKI_FRONT_SERVICE_ID")

introspection_url = f"https://{KEYCLOAK_HOST_IP}/auth/realms/{REALM_NAME}/protocol/openid-connect/token/introspect" \
    if IS_PROD else f'http://{KEYCLOAK_HOST_IP}:{KEYCLOAK_PORT}/auth/realms/{REALM_NAME}/protocol/openid-connect/token/introspect'
discovery_url = f"https://{KEYCLOAK_HOST_IP}/auth/realms/{REALM_NAME}/.well-known/openid-configuration" \
    if IS_PROD else f'http://{KEYCLOAK_HOST_IP}:{KEYCLOAK_PORT}/auth/realms/{REALM_NAME}/.well-known/openid-configuration'

services = {
    ENKI_BACKEND_SERVICE_ID: {
        "url": BACKEND_URI,
        "path": '/enki',
        "bearer_only": 'true',

    },
    ENKI_FRONT_SERVICE_ID: {
        "url": FRONTEND_URI,
        "path": '/front',
        "bearer_only": 'false',
    }
}

for service_id, values in services.items():
    print(f"## {service_id} ## - Start creating service ")
    path = values['path']
    url = values['url']
    bearer_only = values['bearer_only']
    # Add Service for enki URL
    response = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services', data={
        'name': service_id,
        'url': url
    })

    print(f"## {service_id} ## - Results of service creation : {response.json()}")

    created_service_id = response.json()["id"]
    print(f"## {service_id} ## - start creating route with path {values['path']}")
    _ = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services/{ENKI_BACKEND_SERVICE_ID}/routes', data={
        'service.id': f'{created_service_id}',
        'paths[]': path,
    })

    print(f"## {service_id} ## - start configuring OIDC ")
    data = {
        'name': 'oidc',
        'config.client_id': f'{CLIENT_ID}',
        'config.client_secret': f'{CLIENT_SECRET}',
        'config.realm': f'{REALM_NAME}',
        'config.bearer_only': bearer_only,
        'config.introspection_endpoint': introspection_url,
        'config.discovery': discovery_url
    }

    _ = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services/{created_service_id}/plugins', data=data)
    print(f"## {service_id} ## - End")
