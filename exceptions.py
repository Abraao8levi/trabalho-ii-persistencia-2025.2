class BaseCRUDException(Exception):
    """Base exception for CRUD operations."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class NotFoundException(BaseCRUDException):
    """Exception for when a resource is not found."""
    pass

class DuplicateEntryException(BaseCRUDException):
    """Exception for when a duplicate entry is attempted."""
    pass

class ValidationException(BaseCRUDException):
    """Exception for data validation errors."""
    pass