#!/bin/bash

if [ "$1" = "stop" ]; then
    celery multi stop worker --pidfile="./celery.pid"
fi

if [ "$1" = "start" ]; then
    rm -rf ./celery_logs.log
    celery -A worker worker -l info -E -B --pidfile="./celery.pid" --logfile="./celery_logs.log" &
fi

