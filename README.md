# Markino

Markino is the best friend for Lotrèk that can notify you if a server is down, custom scripts, backups and beer.

## Features

- Alarm system: sends an email if the server is down or tests are failing

- Backup/script system: provides a periodic backup system for data and files and scripting


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


## Start Markino

To start Markino use

    $ ./markino.sh start

To stop Markino

    $ ./markino.sh stop

You can find all the logs

    $ tail -f markino.log

## Use command line

To backup a specific project run

    $ python manage.py backup_project my_project_slug

To test a specific project run

    $ python manage.py test_project my_project_slug

To test a specific domain run
	
	$ python manage.py test_domain my_project_slug