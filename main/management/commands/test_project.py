from main.tasks import test_project

from django.core.management.base import BaseCommand, CommandError

from main.models import Project


class Command(BaseCommand):

    help = 'Test a specific project'

    def add_arguments(self, parser):
        parser.add_argument('slug', type=str)

    def handle(self, *args, **options):
        slug = options['slug']
        try:
            project = Project.objects.get(slug=slug)
            test_project(project)
            self.stdout.write(self.style.SUCCESS(
                'Test completed for project "{0}"'.format(slug)
            ))
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Error! Project "{0}" not found'.format(slug)
            ))
