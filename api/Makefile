.PHONY: init init-migration build run db-migrate test tox

init:  build run
	docker-compose exec api sapeur_api db upgrade
	docker-compose exec api sapeur_api init
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

db-migrate:
	docker-compose exec api sapeur_api db migrate

db-upgrade:
	docker-compose exec api sapeur_api db upgrade

test:
	docker-compose stop celery # stop celery to avoid conflicts with celery tests
	docker-compose start rabbitmq redis # ensuring both redis and rabbitmq are started
	docker-compose run -v $(PWD)/tests:/code/tests:ro api tox -e test
	docker-compose start celery

tox:
	docker-compose stop celery # stop celery to avoid conflicts with celery tests
	docker-compose start rabbitmq redis # ensuring both redis and rabbitmq are started
	docker-compose run -v $(PWD)/tests:/code/tests:ro api tox -e py38
	docker-compose start celery

lint:
	docker-compose run web tox -e lint
