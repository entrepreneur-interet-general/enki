build:
	docker-compose -f docker-compose.yml build

build-provision:
	docker-compose -f docker-compose.provision.yml build

setup:
	docker-compose -f docker-compose.yml up -d keycloak-db
	sleep 5
	docker-compose -f docker-compose.yml up -d keycloak
	sleep 10

provision:
	docker-compose -f docker-compose.provision.yml run keycloak-provision
up:
	docker-compose -f docker-compose.yml up

upd:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down --remove-orphans -v

logs:
	docker-compose -f docker-compose.yml logs --follow