import os
import datetime
import requests

from huey import crontab
from huey_logger.decorators import log_db_periodic_task

from main.backup import execute_backup
from main.exceptions import BackupException, FrontendTestException
from main.models import Project, FrontendTest, Report, Deadline, Machine

from django.conf import settings

from main.models import (
    REPORT_TYPE_BACK,
    REPORT_TYPE_TEST,
    REPORT_TYPE_DEADLINE,
    REPORT_TYPE_MACHINE_DEADLINE,
)


def test_project(project):
    report_text = ""
    tests = FrontendTest.objects.filter(project=project)
    headers = {"User-Agent": "whatever"}
    response = requests.get(project.live_url, headers=headers)
    if response.status_code != 200:
        report = Report.objects.create(
            class_type=REPORT_TYPE_TEST,
            project=project,
            text="Server is not responding on {0}".format(project.live_url),
        )
        report.notify()
    for test in tests:
        try:
            test.run()
        except FrontendTestException as ex:
            report_text += "{0}\n".format(ex)
    if report_text:
        report = Report.objects.create(
            class_type=REPORT_TYPE_TEST, project=project, text=report_text
        )
        report.notify()


def backup_project(project):
    if project.backup_active and project.machine:
        try:
            execute_backup(project)
        except BackupException as ex:
            report_text = "{0}\n".format(ex)
            report = Report.objects.create(
                class_type=REPORT_TYPE_BACK, project=project, text=report_text
            )
            report.notify()


def is_in_time_window(date, deltadays=7):
    today = datetime.date.today()
    return date - datetime.timedelta(days=deltadays) < today < date


def check_machines_deadlines():
    machines = Machine.objects.all()

    for machine in machines:
        machine_projects = machine.projects.all()
        if (
            machine.end_time
            and len(machine_projects)
            and is_in_time_window(machine.end_time)
        ):
            report = Report.objects.create(
                class_type=REPORT_TYPE_MACHINE_DEADLINE,
                project=machine_projects[0],
                text="Machine {0} is going to end on {1}".format(
                    machine.name, machine.end_time
                ),
            )
            report.notify()


def check_deadlines(project):
    deadlines = Deadline.objects.filter(project=project)
    for deadline in deadlines:
        if deadline.end_time and is_in_time_window(deadline.end_time):
            report = Report.objects.create(
                class_type=REPORT_TYPE_DEADLINE,
                project=project,
                text="New deadline {0} {1}".format(deadline.end_time, deadline.notes),
            )
            report.notify()


@log_db_periodic_task(crontab(**settings.DEADLINES_SCHEDULE))
def check_all_the_deadlines():
    projects = Project.objects.all()
    for project in projects:
        check_deadlines(project)


@log_db_periodic_task(crontab(**settings.DEADLINES_SCHEDULE))
def check_all_the_machine_deadlines():
    check_machines_deadlines()


@log_db_periodic_task(crontab(**settings.TESTING_SCHEDULE))
def test_projects():
    projects = Project.objects.all()
    for project in projects:
        test_project(project)


@log_db_periodic_task(crontab(**settings.BACKUP_SCHEDULE))
def backup_projects():
    if not os.path.exists(settings.BACKUP_PATH):
        os.makedirs(settings.BACKUP_PATH)
    projects = Project.objects.select_related("machine").all()
    for project in projects:
        backup_project(project)
