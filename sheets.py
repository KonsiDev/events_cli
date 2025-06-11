from __future__ import print_function
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from termcolor import colored

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
RANGE_NAME = 'Eventos!A:I'

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
        try:
            result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
            existing_values = result.get('values', [])
        except Exception as e:
            print(colored(f"Erro ao acessar a planilha: {e}", "red"))
            return

        existing_events_map = {row[0]: {'row_index': i + 1, 'data': row} for i, row in enumerate(existing_values) if row}

        new_events_to_add = []
        events_to_update = []

        for event in events:
            event_name = event[0]
            new_description = event[4]

            if event_name in existing_events_map:
                existing_event = existing_events_map[event_name]
                row_data = existing_event['data']
                row_index = existing_event['row_index']

                has_current_description = len(row_data) > 4 and row_data[4].strip()
                has_new_description = new_description.strip()

                if not has_current_description and has_new_description:
                    update_range = f'Eventos!E{row_index}'
                    events_to_update.append({'range': update_range, 'description': new_description, 'name': event_name})
            else:
                new_events_to_add.append(event)

        if events_to_update:
            print(colored(f"Encontradas {len(events_to_update)} descrições para atualizar...", 'yellow'))
            for item in events_to_update:
                self.sheet.values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=item['range'],
                    valueInputOption='USER_ENTERED',
                    body={'values': [[item['description']]]}
                ).execute()
                print(colored(f"  ✓ Descrição do evento '{item['name']}' atualizada na célula {item['range']}", 'cyan'))
        else:
            print(colored("Nenhuma descrição para atualizar.", 'yellow'))
            
        if new_events_to_add:
            print(colored(f"Adicionando {len(new_events_to_add)} novos eventos...", 'green'))
            self.sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body={'values': new_events_to_add}
            ).execute()
            print(colored(f'  ✓ Novos eventos adicionados com sucesso!', 'green'))
        else:
            print(colored('Nenhum evento novo para adicionar.', 'light_red'))