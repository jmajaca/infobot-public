from datetime import datetime
import uuid


# https://docs.jboss.org/process-guide/en/html/logging.html
class Logger:

    def __init__(self, file_location):
        self.log_file = file_location + '/application_log.log'
        self.trace_file = file_location + '/application_trace.log'

    def new_element_log(self, element, response):
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[%s] New message %s sent to channel %s with link of original post %s.\n' %
                      (str(datetime.now()), str(response['ts']), str(response['channel']), str(element['link'])))

    def info_log(self, text: str):
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[%s] INFO: %s.\n' % (str(datetime.now()), text))

    def error_log(self, e: Exception, **kwargs):
        text = ''
        trace_id = uuid.uuid4().hex
        if kwargs and 'text' in kwargs:
            text = kwargs['text']
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[%s] ERROR: %s. ' % (str(datetime.now()), text + e.__cause__.__str__().replace('\n', '')))
            log.write('For more information see trace.log input with uuid %s.\n' % trace_id)
        self.trace_log(e, trace_id)

    def trace_log(self, e: Exception, trace_id: str):
        with open(self.trace_file, 'a', encoding="utf-8") as trace:
            trace.write('[%s] TRACE: uuid=%s\n' % (str(datetime.now()), trace_id))
            trace.write('%s\n' % str(e))

    def warning_log(self, text: str):
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[%s] WARNING: %s.\n' % (str(datetime.now()), text))

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
