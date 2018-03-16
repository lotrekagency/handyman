from __future__ import print_function
import csv
from django.http import HttpResponse
import os

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_googlecalendarcredentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Cclient_id.jsonedentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart2.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def modify_googleevent(event) :
    
    credentials = get_googlecalendarcredentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    return(event['id']) 

def put_googleevent(event):
  

   
    credentials = get_googlecalendarcredentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    # cerco se evento con quel nome a partire da data di inizio non esiste già
    date=event['start']
    date=date['dateTime'];
    exist = 0
    eventsResult = service.events().list(
        calendarId='primary', timeMin=date,  maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    
   
    
    for event0 in events:
        if (event0['summary'] == event['summary'] ) :
            print()
            exist = 1
   
    if (exist == 0):
        print('inserisco')
        event = service.events().insert(calendarId='marco@lotrek.it', body=event).execute()
        return(event['id'])
    else :
        print('non inserisco')       

    

def export_as_csv_action(description="Export selected objects as CSV file", fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])

        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset

        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset
       
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

        writer = csv.writer(response)

        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            row = [getattr(obj, field)() if callable(getattr(obj, field)) else getattr(obj, field) for field in field_names]
            writer.writerow(row)
        return response

    export_as_csv.short_description = description
    return export_as_csv