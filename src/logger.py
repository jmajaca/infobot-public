from datetime import datetime
from typing import List
from application_log import ApplicationLogType, ApplicationLog
import uuid
import traceback
import re
import os


# https://docs.jboss.org/process-guide/en/html/logging.html
class Logger:
    """
    A class that takes care of logging relevant info for the application

    Attributes
    ----------
    log_file : str
        a path on which application log is located
    trace_file : str
        a path on which trace log (for logging stack trace of errors) is located

    Methods
    -------
    new_element_log(element, response)
        Unused legacy method that logs sending notifications to Slack Workspace
    info_log(text: str)
        Log of events that are of informational nature like (starting, terminating, inserting to db)
        :arg text: str - text that is going to be logged with INFO flag
    error_log(e: Exception, **kwargs)
        Log of events that caused exceptions
        :arg e: Exception - exception that is being logged
        :arg **kwargs: dict - dictionary with possible key 'text' that can contains text that is going to be logged with
        ERROR flag
    trace_log(e: Exception, trace_id: str)
        Saves whole traceback stacktrace in logs
        :arg e: Exception - exception that is being logged
        :arg trace_id: str - unique id which connects ERROR log with newly created TRACE log
    warning_log(text: str)
        Log of events that cause disturbance to normal application operation but do not cause termination of the
        application
        :arg text: str - text that is going to be logged with WARNING flag
    _read_application_log() -> List[str]
        Reads application log and returns list of logs as strings (one row == one application log)
    _read_application_trace() -> List[str]
        Reads trace log and returns list of strings that represent rows in trace log (one row != one trace log)
    get_trace_logs() -> dict
        Returns trace logs as dictionary where every trace log is one element in the dictionary
    get_application_logs() -> List[ApplicationLog]
        Returns application logs as list of ApplicationLog objects sorted by time of the creation
    """

    def __init__(self, file_location=None):
        if file_location is None:
            file_location = os.path.dirname(os.path.realpath(__file__)) + '/log'
        self.log_file = file_location + '/application_log.log'
        self.trace_file = file_location + '/application_trace.log'

    def new_slack_message_log(self, element, response):
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[%s] New message %s sent to channel %s with link of original post %s.\n' %
                      (str(datetime.now()), str(response['ts']), str(response['channel']), str(element['link'])))

    def info_log(self, text: str):
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[%s] INFO: %s\n' % (str(datetime.now()), text))

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
            trace.write('%s\n' % traceback.format_exc())

    def warning_log(self, text: str):
        with open(self.log_file, 'a', encoding="utf-8") as log:
            log.write('[%s] WARNING: %s\n' % (str(datetime.now()), text))

    def _read_application_log(self) -> List[str]:
        with open(self.log_file, 'r', errors='ignore') as log:
            content = log.readlines()
            content = [x.strip().replace('\n', '') for x in content]
            return content

    def _read_application_trace(self) -> List[str]:
        with open(self.trace_file, 'r', errors='ignore') as log:
            content = log.readlines()
            content = [x.strip().replace('\n', '') for x in content]
            return content

    def get_trace_logs(self) -> dict:
        trace_log_lines = self._read_application_trace()
        first = True
        result, uuid = '', ''
        trace_log = dict()
        for line in trace_log_lines + [None]:
            if line is None:
                trace_log[uuid] = result
                break
            uuid_match = re.search(r'uuid=([A-Za-z0-9]+)', line)
            if uuid_match is not None:
                if first:
                    uuid = uuid_match[1]
                    first = False
                else:
                    trace_log[uuid] = result
                    uuid = uuid_match[1]
                    result = ''
            result += line + '\n'
        return trace_log

    def get_application_logs(self) -> List[ApplicationLog]:
        logs = self._read_application_log()
        logs.reverse()
        result: List[ApplicationLog] = []
        for log in logs:
            groups = re.search(r'^\[(.*)\] ([A-Z]+): (.*)$', log)
            if groups is not None:
                if ApplicationLogType(groups[2]) == ApplicationLogType.ERROR:
                    trace_uuid = re.search(r'^.* uuid (.+).$', groups[3])[1]
                    result.append(ApplicationLog(groups[1], ApplicationLogType(groups[2]), groups[3], trace_uuid))
                else:
                    result.append(ApplicationLog(groups[1], ApplicationLogType(groups[2]), groups[3]))
            else:
                result.append(ApplicationLog('', ApplicationLogType.UNKNOWN, log))
        return result
