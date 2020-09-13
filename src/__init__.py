from multiprocessing import Manager
from src.logger import Logger
from src import interrupt_handler
import os

config = dict()


progress_queue = Manager().Queue()
NONE_PROGRESS = 0
INIT_PROGRESS = 5
SCRAPE_PROGRESS = 80
SAVE_PROGRESS = 15
DONE_PROGRESS = 100
progress_queue.put((NONE_PROGRESS, '', 'off'))

current_path = os.path.dirname(os.path.realpath(__file__))

with open(current_path + '/resources/config.cfg') as file:
    for line in file:
        line = line.replace('\n', '')
        elements = line.split('=')
        config[elements[0]] = elements[1]
if config['erase'] == '1':
    with open(current_path + 'resources/config.cfg', 'w') as file:
        file.write('DELETED')

logger = Logger()

interrupt_handler.listen_signals(logger)
