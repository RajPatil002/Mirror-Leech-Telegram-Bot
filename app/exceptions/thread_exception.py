class ThreadException(Exception):
    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.code = code


class DuplicateThread(ThreadException):
    pass

class NoMetadataFound(ThreadException):
    pass
