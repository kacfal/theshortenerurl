format:
	black .

run:
	poetry run python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

test:
	python manage.py test

createsuperuser:
	poetry run python manage.py createsuperuser

.PHONY: format run migrate makemigrations test createsuperuser
