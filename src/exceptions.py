"""
Custom exception definitions for the application.
"""


class BookHiveException(Exception):
    """Base class for all exceptions in the BookHive project."""

    pass


class UserAlreadyExists(BookHiveException):
    """Raised when a user with the same email address already exists."""

    pass


class InvalidCredentials(BookHiveException):
    """Raised when the provided credentials (email and/or password) are invalid."""

    pass


class UserNotFoundException(BookHiveException):
    """Raised when a user is not found."""

    pass


class BookNotFoundException(BookHiveException):
    """Raised when a book is not found."""

    pass
