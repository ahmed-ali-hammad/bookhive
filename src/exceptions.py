"""
Custom exception definitions for the application.
"""


class BookHiveException(Exception):
    """Base class for all exceptions in the BookHive project."""

    pass


class InvalidToken(BookHiveException):
    """Raised when an invalid or expired token is provided."""

    pass


class RevokedToken(BookHiveException):
    """Raised when a token that has been revoked is provided."""

    pass


class AccessTokenRequired(BookHiveException):
    """Raised when a refresh token is provided, but an access token is required."""

    pass


class RefreshTokenRequired(BookHiveException):
    """Raised when an access token is provided, but a refresh token is required."""

    pass


class UserAlreadyExists(BookHiveException):
    """Raised when a user with the same email address already exists."""

    pass


class InvalidCredentials(BookHiveException):
    """Raised when the provided credentials (email and/or password) are invalid."""

    pass


class InsufficientPermission(BookHiveException):
    """Raised when a user doesn't have the necessary permissions to perform an action."""

    pass


class UserNotFoundException(BookHiveException):
    """Raised when a user is not found."""

    pass


class BookNotFoundException(BookHiveException):
    """Raised when a book is not found."""

    pass
