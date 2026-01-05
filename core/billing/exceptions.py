# billing/exceptions.py

class LagoAPIError(Exception):
    def __init__(self, message, response=None):
        self.response = response
        super().__init__(message)
