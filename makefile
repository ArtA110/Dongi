.PHONY: build up down logs shell migrate createsuperuser test lint format restart reset-db

include .env.dev
export $(shell sed 's/=.*//' .env.dev)

DOCKER_COMPOSE = docker compose
PYTHON = docker compose exec backend python
EXEC = docker compose exec
MANAGE = docker compose exec backend python dongi/manage.py 


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
	$(MANAGE) shell


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
	$(EXEC) db psql -U $(SQL_USER) -d postgres -c "DROP DATABASE IF EXISTS $(SQL_DATABASE);"
	$(EXEC) db psql -U $(SQL_USER) -d postgres -c "CREATE DATABASE $(SQL_DATABASE) OWNER $(SQL_USER);"