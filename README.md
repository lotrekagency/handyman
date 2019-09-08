# Handyman

Handyman is the best friend for Lotrèk that can notify you if a server is down, execute custom scripts, make nightly backups and beer 🍻

## Features

- Alarm system: sends an email if the server is down or tests are failing

- Backup/script system: provides a periodic backup system for data and files and scripting

## Configure ENV

Before starting Handyman you need to configure your env: create your env files inside `docker/production/envs` folder (see `docker/production/envs-sample`)

## Start Handyman

    docker-compose -f docker-compose.staging.yml up -d

## Use command line

To backup a specific project run inside `handyman_django` container

    python manage.py backup_project my_project_slug

To test a specific project run

    python manage.py test_project my_project_slug

To test a specific domain run
	
    python manage.py test_domain my_project_slug
