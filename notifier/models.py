from django.db import models

from twilio.rest import Client


class Contact(models.Model):

    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    account = models.CharField(max_length=20, blank=True, null=True)
    token = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    sender = models.BooleanField(default=False)

    def clean(self):
        try:
            Client(self.account, self.token)
            self.sender = True
        except Exception as ex:
            print(ex)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Message(models.Model):

    sender = models.ForeignKey(Contact, related_name="Sender")
    receiver = models.ForeignKey(Contact, related_name="Receiver")

    body = models.TextField()

    def send(self):
        client = Client(self.sender.account, self.sender.token)
        client.messages.create(
            to=self.receiver.phone, from_=self.sender.phone, body=self.body
        )

    def save(self):
        self.send()
