from celery.decorators import periodic_task
from celery.schedules import crontab

from main.models import Project, FrontendTest


@periodic_task(bind=True, run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def test_websites(self):
    projects = Project.objects.all()
    for project in projects:
        tests = FrontendTest.objects.all()
        for test in tests:
            test.run()
