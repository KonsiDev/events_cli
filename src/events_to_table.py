#ler o diretorio do app e encontrar a pasta events.dart
# ler o arquivo e pegar apenas o nome dos eventos (talvez uma descrição)
#Editar a planilha do google sheets
#path C:\Users\andre\Documents\Projetos Flutter\konsi-app

from argparse import ArgumentParser
from .sheets_module.sheets import EventSheets
import os
#ler caminho do argumento
def execute():
    parser = ArgumentParser()
    parser.add_argument('--p', action='store', dest='path', help='Para pegar o caminho do arquivo "events.dart", usar pwd no código do app', required = True)
    arguments = parser.parse_args()
    sheets = EventSheets()

    os.chdir(arguments.path)
    os.chdir('Konsi/lib/src/core/enumerators/analytics')
    # print(os.listdir(os.getcwd()))

    #get events list
    with open('events.dart', 'r')as events_file:
        fileLines = events_file.readlines()
        events_start_index = fileLines.index('enum Events {\n')
        events_end_index = fileLines.index('}\n')#final do enum events
        events = [line for line in fileLines if fileLines.index(line) > events_start_index and fileLines.index(line) < events_end_index]
        events = [event.lstrip().replace('\n', '').replace(',', '') for event in events]
        events = [event.split ('//TODO', 1)[0] for event in events]
        formatted_events = []
        for event in events:
            event_type = ''
            description = ''
            if event.startswith('///DESCRIPTION'):
                description = event.replace('///DESCRIPTION:', '').lstrip()
                descripted_event = events[(events.index(event)+1)]
                if 'click' in descripted_event:
                    event_type = 'Click'
                if 'opened' in descripted_event:
                    event_type = 'View'
                formatted_events.append([descripted_event, '', event_type, description, '', '', '', 'Em desenvolvimento'])
            else:
                if 'click' in event:
                    event_type = 'Click'
                if 'opened' in event:
                    event_type = 'View'
                if all(event not in new_events[0]for new_events in formatted_events):
                    formatted_events.append([event, '', event_type, description, '', '', '', 'Em desenvolvimento'])


    sheets.add_new_events(formatted_events)

if __name__ == '__main__':
    execute()