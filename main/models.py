import requests

from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class LotrekUser(AbstractUser):
    phone_number = PhoneNumberField(blank=True, null=True)


class Project(models.Model):
    name = models.CharField(max_length=200)
    live_url = models.URLField(max_length=400)
    team = models.ManyToManyField(LotrekUser)

    def __str__(self):
        return self.name


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
