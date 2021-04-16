setup:
	docker network create --driver=bridge enki_default

run-app:
	docker-compose -f docker-compose.app.yml up -d --force-recreate

run-gateway:
	docker-compose -f docker-compose.gateway.yml up -d --force-recreate

setup-gateway:
	docker-compose -f docker-compose.gateway.yml run --rm kong kong migrations bootstrap

run-auth:
	docker-compose -f docker-compose.auth.yml up -d --force-recreate