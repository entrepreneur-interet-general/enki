build:
	docker-compose -f docker-compose.yml build

setup:
	docker-compose -f docker-compose.yml up -d kong-db
	sleep 5
	docker-compose -f docker-compose.yml run --rm kong kong migrations up
	sleep 5
	docker-compose -f docker-compose.yml up -d kong

provision:
	docker-compose -f docker-compose.provision.yml run --rm kong-provision

up:
	docker-compose -f docker-compose.yml up kong-db
	docker-compose -f docker-compose.yml up kong

upd:
	docker-compose -f docker-compose.yml up -d kong-db
	docker-compose -f docker-compose.yml up -d kong

down:
	docker-compose -f docker-compose.yml down --remove-orphans -v

logs:
	docker-compose -f docker-compose.yml logs -f