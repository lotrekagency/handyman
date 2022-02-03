from django.test import TestCase

from .models import LotrekUser, Project, Report, FrontendTest

from unittest.mock import patch

from .tasks import test_project


class Response:
    def __init__(self, response, status_code=200):
        self._response = response
        self._status_code = status_code

    @property
    def text(self):
        return self._response

    @property
    def status_code(self):
        return self._status_code


class ReportTest(TestCase):
    def setUp(self):
        lotrek_user = LotrekUser.objects.create(
            id=1,
            username="Marchino",
            first_name="Marco",
            last_name="Bianchi",
            email="lorenzodantonio1995@gmail.com",
            phone_number="+393493084105",
        )

        test_project = Project.objects.create(
            id=1,
            name="Example Project",
            live_url="http://www.google.com",
            domain="google.com",
            backup_active=True,
        )

        test_project.team.add(lotrek_user)

        test_report = Report.objects.create(
            project=Project.objects.get(id__iexact=1),
            text="example report content",
        )

        test_project.team.add(lotrek_user)
        self.test_report = test_report
        self.test_users = LotrekUser.objects.filter(project__in=[test_project])


class FrontendTestTest(TestCase):
    def setUp(self):

        self.test_project = Project.objects.create(
            id=1,
            name="Example Project",
            live_url="http://www.google.com",
            backup_active=True,
        )

        self.test = FrontendTest.objects.create(
            id=1,
            project=self.test_project,
            url=self.test_project.live_url,
            test="IN",
            assertion="Google",
        )

    @patch("main.models.requests.get")
    def test_test(self, mock_request):
        mock_request.return_value = Response("Google")
        test_project(self.test_project)
        assert Report.objects.count() == 0

    @patch("main.models.requests.get")
    def test_test_not_pass(self, mock_request):
        mock_request.return_value = Response("ASD", 404)
        test_project(self.test_project)
        assert Report.objects.count() == 2
        assert (
            Report.objects.filter(
                text="Server is not responding on http://www.google.com"
            ).first()
            is not None
        )
