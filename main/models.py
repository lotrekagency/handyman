import requests

from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    live_url = models.URLField(max_length=400)


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
        if self.test == 'EQ':
            assert text == self.assertion
        if self.test == 'NE':
            assert text != self.assertion
        if self.test == 'IN':
            assert self.assertion in text
        if self.test == 'NI':
            assert self.assertion not in text
