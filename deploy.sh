#!/bin/bash

docker image prune -f

if [ "$1" = "release" ]; then
    docker-compose -f docker-compose.prod.yml build
    docker-compose -f docker-compose.prod.yml stop
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml up -d
fi
