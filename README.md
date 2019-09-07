# Handyman

Handyman is the best friend for Lotrèk that can notify you if a server is down, custom scripts, backups and beer.

## Features

- Alarm system: sends an email if the server is down or tests are failing

- Backup/script system: provides a periodic backup system for data and files and scripting

## Install external software

You need SSHPass and Redis running on your system

## Install requirements

	$ pip install -r requirements.txt

## Override settings

Before starting Markino you may need to override settings: just create local_settings.py file inside markino folder.

	BACKUP_PATH = '/Volumes/EXT_DISK/markino_backup'

## Start Handyman

To start Handyman use

    $ ./handyman.sh start

To stop Handyman

    $ ./handyman.sh stop

You can find all the logs

    $ tail -f handyman.log

## Use command line

To backup a specific project run

    $ python manage.py backup_project my_project_slug

To test a specific project run

    $ python manage.py test_project my_project_slug

To test a specific domain run
	
	$ python manage.py test_domain my_project_slug
