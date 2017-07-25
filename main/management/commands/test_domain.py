from tasks import test_domain

from django.core.management.base import BaseCommand, CommandError

from main.models import Project


class Command(BaseCommand):

    help = 'Test a specific domain'

    def add_arguments(self, parser):
        parser.add_argument('slug', type=str)

    def handle(self, *args, **options):
        slug = options['slug']
        try:
            project = Project.objects.get(slug=slug)
            test_domain(project)
            self.stdout.write(self.style.SUCCESS(
                'Test completed for domain "{0}"'.format(slug)
            ))
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Error! Project "{0}" not found'.format(slug)
            ))
