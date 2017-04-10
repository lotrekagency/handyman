from celery.decorators import periodic_task
from celery.schedules import crontab

from main.backup import execute_backup
from main.exceptions import BackupException, FrontendTestException
from main.models import Project, FrontendTest, Report

from django.conf import settings


@periodic_task(bind=True, run_every=(crontab(**settings.TESTING_SCHEDULE)))
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
            report = Report.objects.create(class_type='TEST', project=project, text=report_text)
            report.notify()


@periodic_task(bind=True, run_every=(crontab(**settings.BACKUP_SCHEDULE)))
def backup_websites(self):
    projects = Project.objects.all()
    for project in projects:
        if project.backup_active:
            try:
                execute_backup(
                    project.slug, project.server_address, project.ssh_username,
                    project.ssh_password, project.backup_script,
                    project.backup_archive, project.backup_sync_folders
                )
            except BackupException as ex:
                report_text = '{0}\n'.format(ex)
                report = Report.objects.create(class_type='BACK', project=project, text=report_text)
                report.notify()
