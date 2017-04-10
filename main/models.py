import requests

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField

from .exceptions import FrontendTestException


class LotrekUser(AbstractUser):
    phone_number = PhoneNumberField(blank=True, null=True)


class Project(models.Model):
    # GENERAL
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    live_url = models.URLField(max_length=400)
    team = models.ManyToManyField(LotrekUser)

    # SSH
    server_address = models.CharField(max_length=200, null=True, blank=True)
    ssh_username = models.CharField(max_length=200, null=True, blank=True)
    ssh_password = models.CharField(max_length=200, null=True, blank=True)

    # BACKUP
    backup_sync_folders = models.TextField(null=True, blank=True)
    backup_archive = models.CharField(max_length=250, null=True, blank=True)
    backup_script = models.TextField(null=True, blank=True)
    backup_active = models.BooleanField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(getattr(self, 'name'))
        super(Project, self).save(*args, **kwargs)


REPORT_TYPES = (
    ('BACK', 'Backup'),
    ('TEST', 'Testing'),
)

class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    class_type = models.CharField(max_length=4, choices=REPORT_TYPES)

    def notify(self):
        print ('* A NEW REPORT! *')

    def __str__(self):
        return self.date.strftime("[{0}] %A, %d. %B %Y %I:%M%p".format(self.class_type))


TEST_CHOICES = (
    ('EQ', 'Is equal'),
    ('NE', 'Not equal'),
    ('IN', 'Contains'),
    ('NI', 'Not contain'),
)


class FrontendTest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    url = models.URLField(max_length=400)
    test = models.CharField(max_length=3, choices=TEST_CHOICES)
    assertion = models.TextField()

    def run(self):
        response = requests.get(self.url)
        text = response.text
        try:
            if self.test == 'EQ':
                assert text == self.assertion
            if self.test == 'NE':
                assert text != self.assertion
            if self.test == 'IN':
                assert self.assertion in text
            if self.test == 'NI':
                assert self.assertion not in text
        except AssertionError:
            assertion_explain = '{0} {1} {2}'.format(self.assertion, self.test, text)
            assertion_explain += '\n\n\n\n'
            raise FrontendTestException(assertion_explain)
