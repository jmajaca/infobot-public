from enum import Enum
from multiprocessing import Manager
from src.logger import Logger
from src import interrupt_handler
import os

config = dict()


progress_queue = Manager().Queue()
none_progress = 0
init_progress = 5
scrape_progress = 80
save_progress = 15
done_progress = 100
progress_queue.put((none_progress, ''))

current_path = os.path.dirname(os.path.realpath(__file__))
log_path = current_path + '/log'

with open(current_path + '/resources/config.cfg') as file:
    for line in file:
        line = line.replace('\n', '')
        elements = line.split('=')
        config[elements[0]] = elements[1]
if config['erase'] == '1':
    with open(current_path + 'resources/config.cfg', 'w') as file:
        file.write('DELETED')

logger = Logger(log_path)

interrupt_handler.listen_signals(logger)
