from django.test import TestCase

from .models import LotrekUser, Project, Report


class ReportTest(TestCase):
	def setUp(self):
		LotrekUser.objects.create(
			id=1,
			username='Marchino',
			first_name='Marco',
			last_name='Bianchi',
			email='info@marco.it',
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

	def test_notify(self):
		project = Projects.objects.get(id__iexact=1)
		project.team.add(LotrekUser.objects.get(id__iexact=1))
		report = Report.objects.get(id__iexact=1)
		report.save()