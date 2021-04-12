setup:
	docker network create --driver=bridge enki_default

run-app:
	docker-compose -f docker-compose.app.yml up -d

run-gateway:
	docker-compose -f docker-compose.gateway.yml up -d

run-auth:
	docker-compose -f docker-compose.auth.yml up -d