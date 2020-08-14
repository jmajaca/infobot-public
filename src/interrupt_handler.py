import signal
import sys
from src import logger
# https://stackoverflow.com/questions/4205317/capture-keyboardinterrupt-in-python-without-try-except

local_logger: logger.Logger


def signal_handler(received_signal, frame):
    if received_signal == signal.SIGINT:
        # local_logger.error_log(KeyboardInterrupt)
        local_logger.info_log('Program finished with exit code 130 (interrupted by signal 2: SIGINT)')
        sys.exit(130)
    elif received_signal == signal.SIGKILL:
        local_logger.info_log('Program finished with exit code 137 (interrupted by signal 9: SIGKILL)')
        sys.exit(137)


def listen_signals(app_logger):
    global local_logger
    local_logger = app_logger
    signal.signal(signal.SIGINT, signal_handler)
    # print('Press Ctrl+C')
    # forever = threading.Event()
    # forever.wait()
