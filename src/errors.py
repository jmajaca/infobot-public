class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class LoginError(Error):

    def __init__(self):
        self.text = 'Could not log in'


class LogoutError(Error):

    def __init__(self):
        self.text = 'Could not log out'
