.PHONY: dev run migrate makemigrations superuser shell test lint docker-up docker-down docker-build

dev:
	docker compose up -d --build
	docker compose exec web python manage.py migrate
	docker compose logs -f web

run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

test:
	python manage.py test

lint:
	pylint problems/

docker-build:
	docker compose build

docker-up:
	docker compose up

docker-down:
	docker compose down
