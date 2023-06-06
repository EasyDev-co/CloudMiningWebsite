run:
	poetry run python manage.py runserver

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

test:
	poetry run python manage.py test

celery:
	poetry run celery -A config worker --beat -s celerybeat-schedule --loglevel INFO

flower:
	poetry run celery -A config flower  --address=127.0.0.1 --port=5566 --loglevel INFO