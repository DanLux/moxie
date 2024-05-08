#!/usr/bin/env bash

python manage.py migrate
python manage.py loaddata users
python manage.py loaddata medspas
python manage.py loaddata services
python manage.py runserver 0.0.0.0:8000