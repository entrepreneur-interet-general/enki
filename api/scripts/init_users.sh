#!/bin/bash

set -e
set -u

set

function create_user_and_database() {
	database=$1
	user=$2
	password=$3

	echo "  Creating user $user and database '$database'"
	PGPASSWORD=${POSTGRES_PASSWORD} psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" -c "CREATE USER $user WITH PASSWORD '$password';"
    PGPASSWORD=${POSTGRES_PASSWORD} psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" -c "CREATE DATABASE $database;"
    PGPASSWORD=${POSTGRES_PASSWORD}  psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" -c "GRANT ALL PRIVILEGES ON DATABASE $database TO $user;"
}

create_user_and_database ${POSTGRES_DB_SAPEUR} ${POSTGRES_USER_SAPEUR} ${POSTGRES_PASSWORD_SAPEUR}
#create_user_and_database prefect prefectadmin prefectpassword
