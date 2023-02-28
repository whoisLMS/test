from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


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


def send_message(service, user_from, user_to, user_subject, user_message):
    message = EmailMessage()

    message.set_content(user_message)

    message['To'] = user_to
    message['From'] = user_from
    message['Subject'] = user_subject

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }

    send_message = (service.users().messages().send
                    (userId='me', body=create_message).execute())
    print(F'Message Id: {send_message["id"]}')


def user_given_parameters():
    user_from = input('Milyen e-mail címről szeretnél e-mailt küldeni?: ')
    user_to = input('Milyen e-mail címre szeretnél e-mailt küldeni?: ')
    user_subject = input('Mi legyen az e-mail tárgya?: ')
    user_message = input(f'Mi álljon az üzenetben?: \n')
    return user_from, user_to, user_subject, user_message


def main():
    service = get_service()
    parameters = user_given_parameters()
    user_from = parameters[0]
    user_to = parameters[1]
    user_subject = parameters[2]
    user_message = parameters[3]
    send_message(service, user_from, user_to, user_subject, user_message)


main()
