from celery.decorators import periodic_task
from celery.schedules import crontab

from main.models import Project, FrontendTest, FrontendTestException, Report
from main.backup import execute_backup

from django.conf import settings


@periodic_task(bind=True, run_every=(crontab(**settings.TESTING_SCHEDULE)))
def test_websites(self):
    print ('start testing')
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


@periodic_task(bind=True, run_every=(crontab(**settings.BACKUP_SCHEDULE)))
def backup_websites(self):
    projects = Project.objects.all()
    for project in projects:
        if project.backup_active:
            execute_backup(
                project.slug, project.server_address, project.ssh_username,
                project.ssh_password, project.backup_script,
                project.backup_archive
            )
