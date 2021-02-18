build:
	docker-compose -f docker-compose.yml build

up:
	docker-compose -f docker-compose.yml up

upd:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down -v --remove-orphans

clean:
	docker-compose -f docker-compose.yml down -v --remove-orphans

logs:
	docker-compose -f docker-compose.yml logs --follow --tail=50

seed:
	docker exec backend_enki-api_1 flask create-position-groups
	docker exec backend_enki-api_1 flask create-groups-and-locations


# Provisions

build-provision:
	docker-compose -f docker-compose.provision.yml build

run-provision:
	docker-compose -f docker-compose.provision.yml run --rm affairs-provision

# Tests

test-resource-up:
	docker-compose -f docker-compose.test.yml up

test-resource-down:
	docker-compose -f docker-compose.test.yml down
