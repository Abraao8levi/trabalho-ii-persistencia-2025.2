class AppException(Exception):
    """Base exception for the application"""
    pass

class NotFoundException(AppException):
    """Resource not found"""
    pass

class DuplicateEntryException(AppException):
    """Duplicate entry violation"""
    pass

class ValidationException(AppException):
    """Validation error"""
    pass

class DatabaseException(AppException):
    """Database operation error"""
    pass