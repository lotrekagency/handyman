from main.tasks import backup_project

from django.core.management.base import BaseCommand

from main.models import Project


class Command(BaseCommand):

    help = "Backup a specific project"

    def add_arguments(self, parser):
        parser.add_argument("slug", type=str)

    def handle(self, *args, **options):
        slug = options["slug"]
        try:
            project = Project.objects.get(slug=slug)
            backup_project(project)
            self.stdout.write(
                self.style.SUCCESS('Backup completed for project "{0}"'.format(slug))
            )
        except Project.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Error! Project "{0}" not found'.format(slug))
            )
