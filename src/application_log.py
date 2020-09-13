from enum import Enum


class ApplicationLogType(Enum):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class ApplicationLog:

    """
    A class that represents an entry from application log of the application

    Attributes
    ----------
    timestamp : str
        date and time when log input was created
    type : ApplicationLogType
        one of three allowed log types
    message:
        message saved in log
    trace_uuid:
        unique identifier which connects ERROR type of log to stack trace
    """

    def __init__(self, timestamp: str, type: ApplicationLogType, message: str, trace_uuid: str = None):
        self.timestamp, self.type, self.message, self.trace_uuid = timestamp, type, message, trace_uuid

    def __repr__(self):
        return "<ApplicationLog(timestamp='%s', type='%s', message='%s', trace_uuid='%s')>" % (
            self.timestamp, self.type, self.message, self.trace_uuid)
