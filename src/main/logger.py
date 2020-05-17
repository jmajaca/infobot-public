from datetime import datetime
import traceback


class Logger:

    def __init__(self, file_location):
        self.file_location = file_location

    def new_element_log(self, element, response, msg_done):
        with open(self.file_location, 'a') as log:
            log.write('[' + str(datetime.now()) + '] New message ' + str(response['ts']) + ' sent to channel ' +
                      str(response['channel']) + ' with link of original post ' + str(element['link']) +
                      '. Current number of messages done is ' + str(len(msg_done)) + '.\n')

    def info_log(self, text):
        with open(self.file_location, 'a') as log:
            log.write('[' + str(datetime.now()) + '] ' + text + '\n')
    # Iteration is done.
    # Program started
    # Program ended

    def error_log(self, e, **kwargs):
        if kwargs and 'text' in kwargs:
            text = kwargs['text']
        else:
            text = 'Error has occurred'
        with open(self.file_location, 'a') as log:
            log.write('[' + str(datetime.now()) + '] ' + text + ': ' + str(e) + '\n')
            log.write(str(traceback.format_exc()) + '\n')
