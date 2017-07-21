from django.test import TestCase

from .models import LotrekUser, Project, Report, FrontendTest
from .exceptions import FrontendTestException

from django.conf import settings

from django.core.mail import send_mail

from unittest.mock import *


class ReportTest(TestCase):
    def setUp(self):
        lotrek_user = LotrekUser.objects.create(
            id=1,
            username='Marchino',
            first_name='Marco',
            last_name='Bianchi',
            email='lorenzodantonio1995@gmail.com',
            phone_number='+393493084105',
        )

        test_project = Project.objects.create(
            id=1,
            name='Example Project',
            live_url='http://www.google.com',
            backup_active=True,
        )

        test_report = Report.objects.create(
            project=Project.objects.get(id__iexact=1),
            text='example report content',
        )

        test_project.team.add(lotrek_user)
        self.test_report = test_report
        self.test_users = LotrekUser.objects.filter(project__in=[test_project])


class Response:

    def __init__(self, response):
        self._response = response

    @property
    def text(self):
        return self._response


class FrontendTestTest(TestCase):

    def setUp(self):

        test_project = Project.objects.create(
            id=1,
            name='Example Project',
            live_url='http://www.google.com',
            backup_active=True,
            )

        self.test = FrontendTest.objects.create(
            id=1,
            project = test_project,
            url=test_project.live_url,
            test='IN',
            assertion='Google',
        )

    @patch('main.models.requests.get')
    def test_test(self, mock_request):
        mock_request.return_value = Response('Google')
        self.test.run()

    @patch('main.models.requests.get')
    def test_test_not_pass(self, mock_request):
        mock_request.return_value = Response('ASD')
        with self.assertRaises(FrontendTestException):
            self.test.run()