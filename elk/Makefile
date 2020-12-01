build:
	docker-compose -f docker-compose.yml build

up:
	docker-compose -f docker-compose.yml up

upd:
	docker-compose -f docker-compose.yml up -d

upd-logstash:
	docker-compose -f docker-compose.logstash.yml up -d

down:
	docker-compose -f docker-compose.yml down --remove-orphans -v

down-logstash:
	docker-compose -f docker-compose.logstash.yml down --remove-orphans -v
logs:
	docker-compose -f docker-compose.yml logs --tail=100 --follow