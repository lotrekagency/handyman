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

from twilio.rest import Client

import csv

from django.http import HttpResponse

from .actions import put_googleevent, get_googlecalendarcredentials, modify_googleevent

class LotrekUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200,null=True, blank=True)
    def __str__(self):
        return self.name 


class Registar(models.Model):
    name = models.CharField(max_length=200)
    panel_registar = models.CharField(max_length=200, null=True, blank=True)
    username_panel_registar = models.CharField(max_length=200, null=True, blank=True)
    password_panel_registar = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name  
        
class Domainregistrant(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200,null=True, blank=True)
    def __str__(self):
        return self.name  

class Domain(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    end_time = models.DateField(null=True, blank=True)
    registar = models.ForeignKey(Registar, null=True, blank=True)
    registrant = models.ForeignKey(Domainregistrant, null=True, blank=True)
    own = models.NullBooleanField(choices=BOOL_CHOICES, null=True, blank=True)
    to_renew = models.NullBooleanField(choices=BOOL_CHOICES, default=True)
    calendar_id = models.CharField(max_length=200,null=True, blank=True)
    
    def save(self, *args, **kwargs):
        date = str(self.end_time)+'T09:00:00-07:00'
        event = {
            'summary': 'Scadenza dominio '+self.name,
            'description': 'scade il dominio, attenzione',
            'start': {
                'dateTime': date,
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': date,
                'timeZone': 'Europe/Rome',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
                ],
            },
            }
        if (self.calendar_id):

       
            event['id']=self.calendar_id
            modify_googleevent(event)

        else :    
          
            if (self.to_renew) :
                self.calendar_id = put_googleevent(event)
        
        super(Domain, self).save(*args, **kwargs)
    def __str__(self):
        return self.name



class Certificateseller(models.Model):
    name = models.CharField(max_length=200)
    panel_seller = models.CharField(max_length=200, null=True, blank=True)
    username_panel_seller = models.CharField(max_length=200, null=True, blank=True)
    password_panel_seller = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name  
        
class Certificate(models.Model):
    name = models.CharField(max_length=200)
    end_time = models.DateField(null=True, blank=True)
    seller = models.ForeignKey(Certificateseller, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    def __str__(self):
        return self.name


class Reseller(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class Machine(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

    name = models.CharField(max_length=200)
    name_on_reseller = models.CharField(max_length=200)
    server_address = models.CharField(max_length=200, null=True, blank=True)
    ssh_username = models.CharField(max_length=200, null=True, blank=True)
    ssh_password = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)
    reseller = models.ForeignKey(Reseller, null=True, blank=True)
    reseller_panel = models.CharField(max_length=200, null=True, blank=True)
    reseller_panel_username = models.CharField(max_length=200, null=True, blank=True)
    reseller_panel_password = models.CharField(max_length=200, null=True, blank=True)
    online_panel = models.CharField(max_length=200)
    online_panel_username = models.CharField(max_length=200, null=True, blank=True)
    online_panel_password = models.CharField(max_length=200, null=True, blank=True)
    root_permissions =  models.BooleanField(choices=BOOL_CHOICES,  default=False)
    management_contract  =  models.BooleanField(choices=BOOL_CHOICES,  default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    calendar_id = models.CharField(max_length=200,null=True, blank=True)
    
    def save(self, *args, **kwargs):
        date = str(self.end_time)+'T09:00:00-07:00'
        event = {
            'summary': 'Scadenza Server '+self.name,
            'description': 'scade il server , attenzione',
            'start': {
                'dateTime': date,
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': date,
                'timeZone': 'Europe/Rome',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
                ],
            },
            }  

        if (self.calendar_id):
            event['id']=self.calendar_id
            modify_googleevent(event)

        else :    
           
            self.calendar_id = put_googleevent(event)
        
        super(Machine, self).save(*args, **kwargs)

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




class Payment(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    domains = models.ManyToManyField(Domain, null=True, blank=True)
    machines = models.ManyToManyField(Machine, null=True, blank=True)
    certificates= models.ManyToManyField(Certificate, null=True, blank=True)
    month = models.DecimalField(max_digits=2, decimal_places=0, null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)
    start_time = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    paid = models.BooleanField(choices=BOOL_CHOICES,  default=False)

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
            print('Failed while contacting {0}'.format(user.username))

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