from src.logger import Logger
from src import interrupt_handler
import os
config = dict()

current_path = os.path.dirname(os.path.realpath(__file__))

with open(current_path + '/resources/config.cfg') as file:
    for line in file:
        line = line.replace('\n', '')
        elements = line.split('=')
        config[elements[0]] = elements[1]
if config['erase'] == '1':
    with open(current_path + 'resources/config.cfg', 'w') as file:
        file.write('DELETED')

logger = Logger(config['log_path'])

interrupt_handler.listen_signals(logger)
