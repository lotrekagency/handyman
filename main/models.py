import time

import requests

from django.core.urlresolvers import reverse

from django.contrib.auth.models import AbstractUser

from django.db import models

from django.conf import settings

from djlotrek import send_mail

from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField

from .exceptions import FrontendTestException


class LotrekUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)


class Reseller(models.Model):
    name = models.CharField(max_length=200)
    # DATI DI ACCESSO RESELLER

    def __str__(self):
        return self.name


class Machine(models.Model):
    name = models.CharField(max_length=200)
    server_address = models.CharField(max_length=200, null=True, blank=True)
    ssh_username = models.CharField(max_length=200, null=True, blank=True)
    ssh_password = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)
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
    ## Folders to do rsync
    backup_sync_folders = models.TextField(null=True, blank=True)
    ## Archive file containing the backup
    backup_archive = models.CharField(max_length=250, null=True, blank=True)
    ## Backup script
    backup_script = models.TextField(null=True, blank=True)
    ## If backup is active for cron jobs
    backup_active = models.BooleanField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(getattr(self, 'name'))
        super(Project, self).save(*args, **kwargs)


REPORT_TYPES = (
    ('BACK', 'Backup'),
    ('TEST', 'Testing'),
    ('I.BS', 'Domain Error')
)

class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    class_type = models.CharField(max_length=4, choices=REPORT_TYPES, blank=True, null=True)

    def notify(self):

        url = reverse('admin:main_report_change', args=[self.id])
        users_emails = LotrekUser.objects.filter(project=self.project).values('email')

        try:
            send_mail(
                settings.DEFAULT_FROM_EMAIL, users_emails,
                '[Report {0}] Markino has a new Report'.format(self.pk),
                context={
                    'link' : url,
                    'description' : self.text
                },
                template_html='mails/report_mail.html',
                template_txt='mails/report_mail.txt',
                fail_silently=settings.DEBUG,
            )
        except Exception as ex:
            print (ex)
            print('Failed while contacting {0}'.format(str(users_emails)))

        time.sleep(1)

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


DEADLINE_TYPES = (
    ('DOM', 'Domain'),
    ('CERT', 'Certificate'),
    ('OTHR', 'Other')
)

class Deadline(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    dead_type = models.CharField(max_length=4, choices=DEADLINE_TYPES, default='OTHR')
    notes = models.TextField(null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.dead_type
