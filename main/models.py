import time
import requests
import json

from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from djlotrek import send_mail
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

from .exceptions import FrontendTestException
from .fields import NonStrippingTextField


class LotrekUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)


class Reseller(models.Model):
    name = models.CharField(max_length=200)
    reseller_panel = models.CharField(max_length=200, null=True, blank=True)
    reseller_panel_username = models.CharField(max_length=200, null=True, blank=True)
    reseller_panel_password = models.CharField(max_length=200, null=True, blank=True)
    # DATI DI ACCESSO RESELLER

    def __str__(self):
        return self.name


class Machine(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    PERIOD= (
    (1, 'Month'),
    (6, 'Semester'),
    (12, 'Year'),
    )
    TYPE= (
    (1, 'Staging'),
    (2, 'Production'),
    )
    name = models.CharField(max_length=200)
    root_permissions =  models.BooleanField(choices=BOOL_CHOICES,  default=False)
    management_contract  =  models.BooleanField(choices=BOOL_CHOICES,  default=True)
    server_address = models.CharField(max_length=200, null=True, blank=True)
    ssh_username = models.CharField(max_length=200, null=True, blank=True)
    ssh_password = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    end_time = models.DateField(null=True, blank=True)
    reseller = models.ForeignKey(Reseller, null=True, blank=True, on_delete=models.SET_NULL)
    administration_panel = models.CharField(max_length=200, null=True, blank=True)
    administration_panel_username = models.CharField(max_length=200, null=True, blank=True)
    administration_panel_password = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_period=models.IntegerField(default=1,choices=PERIOD)
    machine_type=models.IntegerField(default=1,choices=TYPE)
    @property
    def ssh_access(self):
        password = self.ssh_password
        if not password:
            password = "🔑 Use Key"
        if self.server_address and self.ssh_username:
            return "ssh {0}@{1} - pwd: {2}".format(
                self.ssh_username, self.server_address, password
            )

    def __str__(self):
        return self.name


class Project(models.Model):
    # GENERAL
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    live_url = models.URLField(max_length=400)
    team = models.ManyToManyField(LotrekUser)
    machine = models.ForeignKey(Machine, null=True, blank=True, on_delete=models.SET_NULL, related_name='projects')

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


REPORT_TYPE_BACK = 'BACK'
REPORT_TYPE_TEST = 'TEST'
REPORT_TYPE_DEADLINE = 'DEAD'
REPORT_TYPE_MACHINE_DEADLINE = 'MDEA'

REPORT_TYPES = (
    (REPORT_TYPE_BACK, 'Backup'),
    (REPORT_TYPE_TEST, 'Testing'),
    (REPORT_TYPE_DEADLINE, 'Deadline'),
    (REPORT_TYPE_MACHINE_DEADLINE, 'Machine Deadline')
)

class Report(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    class_type = models.CharField(max_length=4, choices=REPORT_TYPES, blank=True, null=True, verbose_name='Type')

    def get_host(self):
        host = getattr(settings, 'HANDYMAN_HOST')
        if not host.endswith('/'):
            host = host + '/'
        return host

    def _get_report_titles(self, url):

        if self.class_type == REPORT_TYPE_BACK:
            return {
                'mail' : '⚠️ #{0} Backup error for {1}'.format(self.pk, self.project.slug),
                'slack' : '⚠️ Backup error for *{0}* @channel: {1}'.format(
                    self.project.slug, url
                )
            }
        if self.class_type == REPORT_TYPE_TEST:
            return {
                'mail' : '❌ #{0} Tests are failing for {1}'.format(self.pk, self.project.slug),
                'slack' : '❌ Tests are failing for *{0}* @channel: {1}'.format(
                    self.project.slug, url
                )
            }
        if self.class_type == REPORT_TYPE_DEADLINE:
            return {
                'mail' : '⏰ #{0} New deadline for {1}'.format(self.pk, self.project.slug),
                'slack' : '⏰ New deadline for *{0}* @channel: {1} {2}'.format(
                    self.project.slug, self.text, url
                ),
                'text' : self.text
            }
        if self.class_type == REPORT_TYPE_MACHINE_DEADLINE:
            return {
                'mail' : '🎰 #{0} New machine deadline for {1}'.format(self.pk, self.project.slug),
                'slack' : '🎰 New machine deadline for *{0}* @channel: {1} {2}'.format(
                    self.project.slug, self.text, url
                ),
                'text' : self.text
            }

    def notify(self):
        import urllib.parse
        users_emails = LotrekUser.objects.filter(project=self.project).values_list('email', flat=True)
        url = urllib.parse.urljoin(self.get_host(), reverse('admin:main_report_change', args=[self.id]))
        report_titles = self._get_report_titles(url)
        try:
            payload = {'text': report_titles['slack']}
            requests.post(
                getattr(settings, 'SLACK_WEBHOOK'),
                data=json.dumps(payload)
            )
        except Exception as ex:
            print (ex)
            print('Failed while contacting {0}'.format(str(users_emails)))
        try:
            context = {'link' : url}
            if 'text' in report_titles:
                context['text'] = report_titles['text']
            send_mail(
                settings.EMAIL_HOST_USER, users_emails,
                report_titles['mail'],
                context=context,
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
    assertion = NonStrippingTextField()


    def _normalize_text(self, text):
        return text.replace('\r\n', '\n').replace('\r', '\n')

    def run(self):
        response = requests.get(self.url)
        text = self._normalize_text(response.text)
        assertion = self._normalize_text(self.assertion)
        try:
            if self.test == 'EQ':
                assert text == assertion
            if self.test == 'NE':
                assert text != assertion
            if self.test == 'IN':
                assert assertion in text
            if self.test == 'NI':
                assert assertion not in text
        except AssertionError:
            assertion_explain = '{0} {1} {2}'.format(assertion, self.test, text)
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
