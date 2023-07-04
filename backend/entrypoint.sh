#!/bin/bash

python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn config.wsgi:application -w 4 --bind 0.0.0.0:8000 --log-level warning