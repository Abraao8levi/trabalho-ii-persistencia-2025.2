class NotFoundException(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)

class DuplicateEntryException(Exception):
    def __init__(self, message: str = "Duplicate entry"):
        self.message = message
        super().__init__(self.message)

class ValidationException(Exception):
    def __init__(self, message: str = "Validation error"):
        self.message = message
        super().__init__(self.message)