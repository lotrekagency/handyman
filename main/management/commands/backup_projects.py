from main.tasks import backup_projects

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = 'Backup all the projects'

    def handle(self, *args, **options):
        try:
            backup_projects()
            self.stdout.write(self.style.SUCCESS(
                'Backup completed for projects'
            ))
        except Exception as ex:
            self.stdout.write(self.style.ERROR('Error!'))
            print (ex)
