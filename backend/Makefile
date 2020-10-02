build:
	docker-compose -f docker-compose.dev.yml build

up:
	docker-compose -f docker-compose.dev.yml up

down:
	docker-compose -f docker-compose.dev.yml down --remove-orphans

ressources: # if you want to get access to postgres but still use your local python
	docker-compose -f docker-compose.ressources.yml up
