
class CanoticError(Exception):

    def __init__(self, message: str, error_code: int):
        self.error_code = error_code
        self.message = message
        super(Exception, self).__init__(f'Canotic API returned {str(self.error_code)}: {self.message}')

class CanoticStorageError(Exception):
    def __init__(self, message: str):
        self.message = message
        super(Exception, self).__init__(f'Canotic Storage service failed: {self.message}')