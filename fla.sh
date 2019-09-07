#!/bin/bash

# Migrate the database
while !</dev/tcp/db/5432; do sleep 1; done;

python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic --noinput

./gunicorn.sh start
