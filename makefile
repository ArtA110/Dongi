.PHONY: build up down logs shell migrate createsuperuser test lint format


DOCKER_COMPOSE = docker compose
PYTHON = docker compose exec backend python


build:
	$(DOCKER_COMPOSE) up --build -d


up:
	$(DOCKER_COMPOSE) up -d


down:
	$(DOCKER_COMPOSE) down


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
