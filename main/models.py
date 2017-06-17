import requests

from django.contrib.auth.models import AbstractUser

from django.db import models
from django.core.mail import send_mail
from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField

from .exceptions import FrontendTestException

from twilio.rest import Client


class LotrekUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)


class Reseller(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Machine(models.Model):
    name = models.CharField(max_length=200)
    server_address = models.CharField(max_length=200, null=True, blank=True)
    ssh_username = models.CharField(max_length=200, null=True, blank=True)
    ssh_password = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    reseller = models.ForeignKey(Reseller, null=True, blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    # GENERAL
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    live_url = models.URLField(max_length=400)
    team = models.ManyToManyField(LotrekUser)
    machine = models.ForeignKey(Machine, null=True, blank=True)

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    class_type = models.CharField(max_length=4, choices=REPORT_TYPES, blank=True, null=True)

    def notify(self):
        print ('* A NEW REPORT! *')

    def send_sms(self, to=[]):
        client = Client('ACdb1b5f26c8aed5cc39461306a9c700da', '58a3e10ef80d19f88692342d87bc4e97')

        for num in to:
            client.messages.create(to=num, from_='+14158422892', body=self.text)

    def save(self, *args, **kwargs):
        users = LotrekUser.objects.filter(project=self.project)

        phone_nums = []

        for user in users:
            phone_nums.append(user.phone_number)
            print([user.email for user in users])

        send_mail(
            'Report',
            self.text,
            'lorenzodantonio1995@gmail.com',
            ['lorenzodantonio1995@gmail.com'],
            #[user.email for user in users],
            fail_silently=False,
            )
        self.send_sms(phone_nums)

        super(Report, self).save(*args, **kwargs)

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
