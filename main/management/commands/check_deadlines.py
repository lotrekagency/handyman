from tasks import check_deadlines

from django.core.management.base import BaseCommand, CommandError

from main.models import Project


class Command(BaseCommand):

    help = 'check deadlines for a specific project'

    def add_arguments(self, parser):
        parser.add_argument('slug', type=str)

    def handle(self, *args, **options):
        slug = options['slug']
        try:
            project = Project.objects.get(slug=slug)
            check_deadlines(project)
            self.stdout.write(self.style.SUCCESS(
                'All deadlines checked for "{0}"'.format(slug)
            ))
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Error! Project "{0}" not found'.format(slug)
            ))
