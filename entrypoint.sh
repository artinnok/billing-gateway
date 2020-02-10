#!/bin/bash

sleep 5

python manage.py migrate
gunicorn config.wsgi --bind 0.0.0.0:9000