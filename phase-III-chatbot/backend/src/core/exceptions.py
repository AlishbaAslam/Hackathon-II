"""
Custom exception classes for the backend.
"""
from typing import Optional
from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    """Exception raised for unauthorized access attempts."""
    def __init__(self, detail: str = "Unauthorized: Invalid or missing credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(HTTPException):
    """Exception raised when user doesn't have permission to access a resource."""
    def __init__(self, detail: str = "Forbidden: Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class NotFoundException(HTTPException):
    """Exception raised when a requested resource is not found."""
    def __init__(self, detail: str = "Not Found: The requested resource does not exist"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ConflictException(HTTPException):
    """Exception raised when there's a conflict with the current state."""
    def __init__(self, detail: str = "Conflict: The request conflicts with the current state"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class ValidationException(HTTPException):
    """Exception raised for validation errors."""
    def __init__(self, detail: str = "Validation Error: Request data is invalid"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )