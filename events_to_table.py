from argparse import ArgumentParser
from sheets import EventSheets
import os

def execute():
    parser = ArgumentParser()
    parser.add_argument('--file-path', dest='file_path', help='Caminho para o arquivo events.dart', required=True)
    arguments = parser.parse_args()

    sheets = EventSheets()

    if not os.path.exists(arguments.file_path):
        print(f"Erro: O arquivo em '{arguments.file_path}' não foi encontrado.")
        return

    #get events list
    with open(arguments.file_path, 'r') as events_file:
        fileLines = events_file.readlines()
        events_start_index = fileLines.index('enum Events {\n')
        events_end_index = fileLines.index('}\n')
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
                formatted_events.append([descripted_event,'', '', event_type, description, '', '', '', 'Em desenvolvimento'])
            else:
                if 'click' in event:
                    event_type = 'Click'
                if 'opened' in event:
                    event_type = 'View'
                if all(event not in new_events[0]for new_events in formatted_events):
                    formatted_events.append([event,'', '', event_type, description, '', '', '', 'Em desenvolvimento'])


    sheets.add_new_events(formatted_events)

if __name__ == '__main__':
    execute()