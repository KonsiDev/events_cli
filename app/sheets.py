from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '11v2Dd4rG4E8uXnxZWXK5ZXfwwljX7xkLp_iRXdur2To'
RANGE_NAME = 'Eventos!A1:H'

class EventSheets:
    def __init__(self) -> None:
        self.sheet = self.set_credentials()

    def set_credentials(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0, success_message='Autenticado com sucesso, pode fechar esta aba.')
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        return service.spreadsheets()

    
    def add_new_events(self, events: list):
        #get old table events
        result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            #echo no values found
            print('echo')
        new_events = []
        for event in events:
            if all(event[0] not in row[0] for row in values):
                new_events.append(event)
        if len(new_events) != 0:
            new_events_index = len(values)+1
            self.sheet.values().update(spreadsheetId= SPREADSHEET_ID, range=f'Eventos!A{new_events_index}:H', valueInputOption='USER_ENTERED', body = {'values': new_events}).execute()
        else:
            print ('sem novos eventos')

if __name__ == '__main__':
    sheets = EventSheets()
    sheets.set_credentials()
    sheets.add_new_events([])