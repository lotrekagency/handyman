import os
import requests
import datetime

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from main.backup import execute_backup
from main.exceptions import BackupException, FrontendTestException
from main.models import Project, FrontendTest, Report

from django.conf import settings

from main.models import Report, Project, LotrekUser, Deadline, Machine


def test_project(project):
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


def backup_project(project):
    if project.backup_active and project.machine:
        try:
            execute_backup(project)
        except BackupException as ex:
            report_text = '{0}\n'.format(ex)
            report = Report.objects.create(class_type='BACK', project=project, text=report_text)
            report.notify()


def check_machines_deadlines():
    machines = Machine.objects.all()
    today = datetime.date.today()
    for machine in machines:
        if machine.end_time and machine.end_time - datetime.timedelta(days=7) < today < machine.end_time:
            print ('SCADE!')


def check_deadlines(project):
    deadlines = Deadline.objects.filter(project=project)
    today = datetime.date.today()
    for deadline in deadlines:
        if deadline.end_time and deadline.end_time - datetime.timedelta(days=7) < today < deadline.end_time:
            print ('SCADE!')


@db_periodic_task(crontab(hour='*/1'))
def test_projects():
    print ('ES')
    projects = Project.objects.all()
    for project in projects:
        test_project(project)


@db_periodic_task(crontab(**settings.BACKUP_SCHEDULE))
def backup_projects():
    print ('Start Backup')
    print (settings.BACKUP_SCHEDULE)
    if not os.path.exists(settings.BACKUP_PATH):
        os.makedirs(settings.BACKUP_PATH)
    projects = Project.objects.select_related('machine').all()
    for project in projects:
        backup_project(project)
    print ('End Backup')
