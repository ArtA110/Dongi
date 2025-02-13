.PHONY: build up down logs shell migrate createsuperuser test lint format


DOCKER_COMPOSE = docker compose
PYTHON = docker compose exec backend python
EXEC = docker compose exec


build:
	$(DOCKER_COMPOSE) up --build -d


up:
	$(DOCKER_COMPOSE) up -d


down:
	$(DOCKER_COMPOSE) down


restart:
	$(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d


logs:
	$(DOCKER_COMPOSE) logs -f


shell:
	$(PYTHON) sh


migrate:
	$(PYTHON) dongi/manage.py migrate


createsuperuser:
	$(PYTHON) dongi/manage.py createsuperuser


test:
	$(PYTHON) dongi/manage.py test


lint:
	$(PYTHON) -m ruff check dongi


format:
	$(PYTHON) -m ruff format dongi


reset-db:
	$(EXEC) db psql -U dev -d postgres -c "DROP DATABASE IF EXISTS dongi;"
	$(EXEC) db psql -U dev -d postgres -c "CREATE DATABASE dongi OWNER dev;"