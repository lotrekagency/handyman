import requests

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField


class LotrekUser(AbstractUser):
    phone_number = PhoneNumberField(blank=True, null=True)


class Project(models.Model):
    # GENERAL
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    live_url = models.URLField(max_length=400)
    team = models.ManyToManyField(LotrekUser)

    # SSH
    server = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)

    # BACKUP
    backup_archive = models.CharField(max_length=250, null=True, blank=True)
    backup_script = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(getattr(self, 'name'))
        super(Project, self).save(*args, **kwargs)


class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def notify(self):
        pass

    def __str__(self):
        return self.date.strftime("%A, %d. %B %Y %I:%M%p")


TEST_CHOICES = (
    ('EQ', 'Is equal'),
    ('NE', 'Not equal'),
    ('IN', 'Contains'),
    ('NI', 'Not contain'),
)


class FrontendTestException(Exception):
    pass


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
