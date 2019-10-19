from main.tasks import backup_project

from django.core.management.base import BaseCommand, CommandError

from main.models import Project


class Command(BaseCommand):

    help = 'Backup all the projects'

    def handle(self, *args, **options):
        try:
            projects = Project.objects.select_related('machine').all()
            for project in projects:
                backup_project(project)
            self.stdout.write(self.style.SUCCESS(
                'Backup completed for projects'
            ))
        except Exception as ex:
            self.stdout.write(self.style.ERROR('Error!'))
            print (ex)
