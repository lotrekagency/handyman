import os

from celery.decorators import periodic_task
from celery.schedules import crontab

from main.backup import execute_backup
from main.exceptions import BackupException, FrontendTestException
from main.models import Project, FrontendTest, Report

from django.conf import settings


@periodic_task(
    bind=True,
    run_every=(crontab(**settings.TESTING_SCHEDULE)),
    default_retry_delay=30, max_retries=3,
    soft_time_limit=500
)
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


@periodic_task(
    bind=True,
    run_every=(crontab(**settings.BACKUP_SCHEDULE)),
    default_retry_delay=30, max_retries=3,
    soft_time_limit=500
)
def backup_websites(self):
    if not os.path.exists(settings.BACKUP_PATH):
        os.makedirs(settings.BACKUP_PATH)
    projects = Project.objects.select_related('machine').all()
    for project in projects:
        if project.backup_active and project.machine:
            try:
                execute_backup(
                    project.slug,
                    project.machine.server_address,
                    project.machine.ssh_username,
                    project.machine.ssh_password,
                    project.backup_script,
                    project.backup_archive,
                    project.backup_sync_folders
                )
            except BackupException as ex:
                report_text = '{0}\n'.format(ex)
                report = Report.objects.create(class_type='BACK', project=project, text=report_text)
                report.notify()
