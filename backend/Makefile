build:
	docker-compose -f docker-compose.yml build

up:
	docker-compose -f docker-compose.yml up

upd:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down --remove-orphans

logs:
	docker-compose -f docker-compose.yml logs --follow


# Provisions

build-provision:
	docker-compose -f docker-compose.provision.yml build

run-provision:
	docker-compose -f docker-compose.provision.yml run --rm affairs-provision
