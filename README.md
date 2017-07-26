# Markino

Markino is the best friend that can notify you is a server is down. Also it offers you backups and beer.

## Features

- Alarm system: sends an sms and/or an email if the server is down or tests are failing

- Backup system: provides a periodic backup system for data and files


## Install SSHPass on youy system

- Debian-base:
	$ sudo apt-get install sshpass

- RHEL/CentOS Linux
	$ sudo yum install sshpass

- Fedora
	$ sudo dnf install sshpass

- Arch Linux
	$ sudo pacman -S sshpass

- OpenSUSE
	$ sudo zypper install sshpass

- FreeBSD
	$ cd /usr/ports/security/sshpass/ && make install clean
	$ pkg install sshpass


## Use Celery

To start celery

    $ ./celery.sh start

To stop celery

    $ ./celery.sh stop

You can find all the logs

    $ tail -f celery_logs.log

## Use command line

To backup a specific project run

    $ python manage.py backup_project my_project_slug

To test a specific project run

    $ python manage.py test_project my_project_slug

To test a specific domain run
	
	$ python manage.py test_domain my_project_slug