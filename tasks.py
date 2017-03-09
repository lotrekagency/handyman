from celery.decorators import periodic_task
from celery.schedules import crontab

from main.models import Project, FrontendTest, FrontendTestException, Report


@periodic_task(bind=True, run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def test_websites(self):
    projects = Project.objects.all()
    for project in projects:
        report_text = ''
        tests = FrontendTest.objects.all()
        for test in tests:
            try:
                test.run()
            except FrontendTestException as ex:
                report_text += '{0}\n'.format(ex)
        if report_text:
            report = Report.objects.create(project=project, text=report_text)
            report.notify()
