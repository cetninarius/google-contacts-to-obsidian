from __future__ import print_function

import json

from jinja2 import Template
import codecs

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts']


def get_google_contacts():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)

        creds = flow.run_local_server(port=42047)  # match port according to redirect uri for localhost
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('people', 'v1', credentials=creds)

        # Call the People API
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,
            personFields='names,emailAddresses,organizations,phoneNumbers,biographies,relations,birthdays,events,addresses').execute()
        connections = results.get('connections', [])

        return connections

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    # delete all old files
    if os.path.exists('vault'):
        for filename in os.listdir('vault'):
            if os.path.isfile(os.path.join('vault', filename)):
                os.remove(os.path.join('vault', filename))
    else:
        os.mkdir('vault')

    connections = get_google_contacts()

    for person in connections:

        names = person.get('names', [])

        if names:
            try:
                name = names[0].get('givenName') + ' ' + names[0].get('familyName')
                print(name)
            except:
                name = names[0].get('displayName')

            # render the template
            with open('t_person.md', 'r') as file:
                template = Template(file.read(), trim_blocks=True)
            rendered_file = template.render(repo=person)

            # output the file
            output_file = codecs.open("vault/{}.md".format(name).strip(), "w", "utf-8")
            output_file.write(rendered_file)
            output_file.close()
