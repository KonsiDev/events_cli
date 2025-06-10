from __future__ import print_function
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from termcolor import colored

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
RANGE_NAME = 'Eventos!A1:H'

class EventSheets:
    def __init__(self) -> None:
        self.sheet = self.set_credentials()

    def set_credentials(self):
        gcp_sa_key_content = os.environ.get('GCP_SA_KEY')
        if not gcp_sa_key_content:
            raise ValueError("A variável de ambiente EVENTS_CLI_GCP_SA_KEY não foi definida.")

        if not SPREADSHEET_ID:
            raise ValueError("A variável de ambiente EVENTS_CLI_SPREADSHEET_ID não foi definida.")

        creds_json = json.loads(gcp_sa_key_content)
        
        creds = service_account.Credentials.from_service_account_info(creds_json, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=creds)
        return service.spreadsheets()
    
    def add_new_events(self, events: list):

        result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            print(colored('Tabela não encontrada', 'red'))
        new_events = []
        for event in events:
            if all(event[0] not in row[0] for row in values):
                new_events.append(event)
        if len(new_events) != 0:
            new_events_index = len(values)+1
            last_index = new_events_index + (len(new_events)-1)
            self.sheet.values().update(spreadsheetId= SPREADSHEET_ID, range=f'Eventos!A{new_events_index}:I', valueInputOption='USER_ENTERED', body = {'values': new_events}).execute()
            print(colored(f'Adicionados eventos do index {new_events_index} ao {last_index}', 'green'))
        else:
            print (colored('sem novos eventos', 'light_red'))
