from django.test import TestCase

from .models import LotrekUser, Project, Report
from django.core.mail import send_mail

from unittest.mock import *


class ReportTest(TestCase):
    def setUp(self):
        LotrekUser.objects.create(
            id=1,
            username='Marchino',
            first_name='Marco',
            last_name='Bianchi',
            email='lorenzodantonio1995@gmail.com',
            phone_number='+393493084105',
        )

        Project.objects.create(
            id=1,
            name='Example Project',
            live_url='http://www.google.com',
            backup_active=True,
            )

        Report.objects.create(
            project=Project.objects.get(id__iexact=1),
            text='example report content',
        )

        self.test_project = Project.objects.get(id__iexact=1)
        self.test_users = LotrekUser.objects.filter(project=self.test_project)
        self.test_phone = [user.phone_number for user in self.test_users]

    @patch('main.models.Report.send_sms')
    def test_notify(self, mock_send_sms):
        mock_send_sms.assert_called_with(self.test_phone)