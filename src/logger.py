from datetime import datetime
import traceback
import uuid


# https://docs.jboss.org/process-guide/en/html/logging.html
class Logger:

    def __init__(self, file_location):
        self.log_file = file_location + '/application_log.log'
        self.trace_file = file_location + '/application_trace.log'

    def new_element_log(self, element, response, msg_done):
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[' + str(datetime.now()) + '] New message ' + str(response['ts']) + ' sent to channel ' +
                      str(response['channel']) + ' with link of original post ' + str(element['link']) +
                      '. Current number of messages done is ' + str(len(msg_done)) + '.\n')

    def info_log(self, text):
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[' + str(datetime.now()) + '] INFO: ' + text + '\n')

    def error_log(self, e, **kwargs):
        text = ''
        if kwargs and 'text' in kwargs:
            text = kwargs['text']
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[' + str(datetime.now()) + '] ERROR: ' + text + str(e) + '\n')
        self.trace_log(e)

    def trace_log(self, e):
        trace_id = uuid.uuid4().hex
        text = 'See trace.log input with uuid ' + str(trace_id) + ' for more information.'
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[' + str(datetime.now()) + '] TRACE: ' + text + '\n')
        with open(self.trace_file, 'a', encoding="utf-8") as trace:
            trace.write('[' + str(datetime.now()) + '] TRACE: uuid=' + str(trace_id) + '\n')
            trace.write(str(traceback.format_exc()) + '\n')

    def warning_log(self, text):
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[' + str(datetime.now()) + '] WARNING: ' + text + '\n')

    def read_application_log(self):
        with open(self.log_file, 'r', errors='ignore') as log:
            content = log.readlines()
            content = [x.strip()[:-1] if x[-1] == '\n' else x.strip() for x in content]
            return content

    def read_application_trace(self):
        with open(self.trace_file, 'r', errors='ignore') as log:
            content = log.readlines()
            content = [x.strip()[:-1] if x[-1] == '\n' else x.strip() for x in content]
            return content
