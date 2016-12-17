from celery.decorators import periodic_task
import os, time
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'markino.settings')

app = Celery('markino')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(bind=True, run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def test_websites(self):
    print ('ciao')
