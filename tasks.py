import os
import requests
import datetime

from celery.decorators import periodic_task
from celery.schedules import crontab

from main.backup import execute_backup
from main.exceptions import BackupException, FrontendTestException
from main.models import Project, FrontendTest, Report

from django.conf import settings

from main.models import Report, Project, LotrekUser


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


def test_domain(project):
    domain = project.domain

    url = '{0}Info?ApiKey={1}&Password={2}&Domain={3}&ResponseFormat={4}'.format(
        settings.IBS_BASE_URL,
        settings.IBS_API_KEY,
        settings.IBS_API_PWD,
        domain,
        settings.IBS_DEFAULT_FORMAT,
    )

    try:
        response = requests.get(url, timeout=10).json()
        status = response['status']

        if status == 'FAILURE':
            print(status)
            return

    except requests.exceptions.RequestException as ex:
        print(ex)
        return

    status = response['status']
    domain_status = response['domainstatus']

    if domain_status == 'EXPIRED':
        message = 'Domain {0} expired'.format(domain)
        report = Report.objects.create(class_type='I.BS', project=project, text=message)
        report.notify()
        project.managed = False

    else:
        try:
            expiration = (response['expirationdate'].split('/'))
        except Exception as ex:
            message = 'Cannot verify domain {0}. EXCEPTION: {1}'.format(domain, ex)
            report = Report.objects.create(class_type='I.BS', project=project, text=message)
            report.notify()
            project.managed = False
            print(ex, message)

        expire_year = int(expiration[0])
        expire_month = int(expiration[1])
        expire_day = int(expiration[2])

        expiration_date = datetime.date(
            expire_year,
            expire_month,
            expire_day,
        )

        today_date = datetime.date.today()

        days_to_expiration = expiration_date - today_date

        if days_to_expiration <= datetime.timedelta(30):
            message = '{0} days to {1} expiration'.format(days_to_expiration, domain)
            report = Report.objects.create(class_type='I.BS', project=project, text=message)
            report.notify()
            project.managed = False

        else:
            print('(domain={0}, expiration date={1}) OK'.format(domain, expiration_date))


@periodic_task(
    bind=True,
    run_every=(crontab(**settings.TESTING_SCHEDULE)),
    default_retry_delay=30, max_retries=3,
    soft_time_limit=500,
)
def test_projects(self):
    projects = Project.objects.all()
    for project in projects:
        test_project(project)


@periodic_task(
    bind=True,
    run_every=(crontab(**settings.BACKUP_SCHEDULE)),
    default_retry_delay=30, max_retries=3,
    soft_time_limit=500
)
def backup_projects(self):
    if not os.path.exists(settings.BACKUP_PATH):
        os.makedirs(settings.BACKUP_PATH)
    projects = Project.objects.select_related('machine').all()
    for project in projects:
        backup_project(project)

@periodic_task(
    bind=True,
    run_every=(crontab(**settings.TESTING_SCHEDULE)),
    default_retry_delay=30, max_retries=3,
    soft_time_limit=500
)
def test_domains(self):
    domains = [test_domain(project.domain) for project in Project.objects.filter(managed=False)]