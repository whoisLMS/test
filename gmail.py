from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service


def get_messages(service, given_times_index, given_type_index):
    results = service.users().messages().list(userId='me').execute()
    msg_ids = []
    for msg in results['messages']:
        msg_ids.append(msg['id'])
    for index in range(given_times_index):
        message = service.users().messages().get(userId='me',
                                                 id=msg_ids[index], format='metadata').execute()
        headers = message['payload']['headers']
        for header in headers:
            if given_type_index == 1:
                if header['name'] == 'From':
                    print(f'From: {header["value"]}')
            if given_type_index == 2:
                if header['name'] == 'Subject':
                    print(f'Subject: {header["value"]}')
            if given_type_index == 3:
                if header['name'] == 'Date':
                    print(f'\nDate: {header["value"]}')


def give_indexes():
    given_times_index = int(input("Hány leveledről szeretnél információkat? (csak a szám kell!): "))
    given_type_index = int(input(f"Mit szeretnél megtudni ezekről a levelekről?"
                                 f"\nKitől jött - 1\nA levél témája - 2\nA levél dátuma - 3     "))
    return given_times_index, given_type_index


def main():
    given_indexes = give_indexes()
    given_times_index = given_indexes[0]
    given_type_index = given_indexes[1]
    service = get_service()
    get_messages(service, given_times_index, given_type_index)


main()
