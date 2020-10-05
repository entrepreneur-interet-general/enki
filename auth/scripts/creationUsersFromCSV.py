import requests
import urllib3
from keycloak import KeycloakAdmin
import csv
from pathlib import Path
from datetime import datetime

import configparser # Permet de parser le fichier de paramètres
config = configparser.RawConfigParser() # On créé un nouvel objet "config"
config.read('creation-utilisateur.conf')

urllib3.disable_warnings()

# Login with role admin
def login_as_admin(serverUrl, username, password):
    keycloak_admin = KeycloakAdmin(server_url=serverUrl,
                                   username=username,
                                   password=password,
                                   realm_name='master',
                                   verify=False)
    return keycloak_admin

# Add user and set password
def create_keycloak_user(keycloak_admin, userName, firstName, lastName, num_matricule, password):
    new_user = keycloak_admin.create_user({"email": "",
                                           "username": userName,
                                           "enabled": True,
                                           "firstName": firstName,
                                           "lastName": lastName,
                                           "attributes": {"matricule": num_matricule},
                                           "credentials": [{"value": password, "type": "password"}],
                                           "requiredActions": ["UPDATE_PASSWORD"]
                                           })
    return new_user

# Create request
def create_role(apiServerUrl, apiKey, matricule, roles):
    payload = roles.split('//')
    headers = {
        "x-api-key": apiKey
    }

    r = requests.put(apiServerUrl + "/v0/agents/" + matricule + "/roles", json=payload, headers=headers, verify=False)

    if r.status_code == 400:
        raise Exception('Mauvais format de roles ou role inexistant sur l\'api,\n\t' + r.json()['message'])
    elif r.status_code > 400 and r.status_code < 500:
        raise Exception('Code : '+ r.status_code + ' Message : '+ r.json()['message'])
    r.raise_for_status()

# Retrieve CSV file
# Give this file path just after python file execution exmpale :  python3 creationUsersFromCSV.py ~/Téléchargements/agents.csv

def retrieve_file_path(csv_file_path):

    filename = Path(csv_file_path)

    data_folder_path = csv_file_path.replace(filename.name, '')
    data_folder = Path(data_folder_path)

    file_to_open = data_folder / filename.name
    return file_to_open

# Read file csv
def readCsvFile(file_to_open):
    try:
        csvfile = open(file_to_open, 'rt')
    except:
        print("File not found")

    input_file = csv.DictReader(csvfile)
    return input_file


class UserRecap:
    def __init__(self, username, matricule):
        self.username = username
        self.matricule = matricule
        self.keycloak = "OK"
        self.roles = "OK"

# Main code

args={
    'keycloakServerUrl'     : config.get('KEYCLOAK','serverUrl'),
    'keycloakUsername'   : config.get('KEYCLOAK','username'),
    'keycloakPassword'   : config.get('KEYCLOAK','password'),
    'apiRolesServerUrl'     : config.get('API','serverUrl'),
    'apiRolesKey'        : config.get('API','privateKey'),
    'filename'           : config.get('FICHIER UTILISATEUR','filename')
}

# Prompt for csv file
admin = login_as_admin(args['keycloakServerUrl'], args['keycloakUsername'], args['keycloakPassword'])
admin.realm_name = 'nexsis'
file = retrieve_file_path(args['filename'])
data = readCsvFile(file)


totalRows = 0
successRows = 0
recap = []
print("========================================")
print("===============  GO  ===================")
print("========================================\n")

for row  in data:
    totalRows += 1
    currentUser = UserRecap(row.get('userName'), row.get('matricule'))

    print('INFO - creation de : ' + row.get('firstName') + ' ' + row.get('lastName'))
    try:
        create_keycloak_user(admin, row.get('userName'), row.get('firstName'), row.get('lastName'), row.get('matricule'), row.get('password'))
    except Exception as err:
        if err.response_code == 409:
            print('INFO - deja dans keycloak avec le même username ' + row.get('userName'))
        else:
            currentUser.keycloak = "KO"
            print('ERROR - {0}'.format(err))
    pass
    try:
        create_role(args['apiRolesServerUrl'], args['apiRolesKey'], row.get('matricule'), row.get('roles'))
        successRows += 1
        print('INFO - '+row.get('firstName') + ' ' + row.get('lastName') + ' a été crée')
    except Exception as err:
        currentUser.roles = "KO"
        print('ERROR - {0}'.format(err))
        print('ERROR - erreur lors de la création de : ' + row.get('firstName') + ' ' + row.get('lastName'))
    pass

    recap.append(currentUser)
    print('------------------------------')

print("========================================")
print("===============  RECAP  ================")
print("========================================\n")


now = datetime.now()
date_time = now.strftime("%d-%m-%Y_%H-%M-%S")

# Filename to write
filename = date_time + "_report.csv"

# Open the file with writing permission
myfile = open(filename, 'w')

# Write a line to the file
myfile.write("userName;matricule;keycloak;roles\n")

for user in recap:
    myfile.write("{0};{1};{2};{3}\n".format(user.username,user.matricule, user.keycloak, user.roles))


# Close the file
myfile.close()

print("Le rapport " + filename + " à été généré")
print(str(successRows) + ' utilisateur(s) ajouté(s) sur ' + str(totalRows))

