from main.tasks import check_machines_deadlines

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "check deadlines for all machines"

    def handle(self, *args, **options):
        check_machines_deadlines()
        self.stdout.write(self.style.SUCCESS("All machines deadlines checked"))
