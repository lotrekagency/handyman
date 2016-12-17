import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'markino.settings')
django.setup()

from celery import Celery

from django.conf import settings


app = Celery('markino')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from tasks import test_websites
