#!/bin/bash


if [ "$1" = "start" ]; then
    gunicorn $PROJECT_NAME.wsgi -c gunicorn_settings.py --name gunicorn_$PROJECT_NAME --timeout=500 --graceful-timeout=500
fi

if [ "$1" = "restart" ]; then
    sleep 2
    ps aux | grep gunicorn_$PROJECT_NAME | awk '{ print $2 }' | xargs kill -HUP
fi
