"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.core.dependencies import get_current_user
from src.models.user import User
from src.services.auth_service import (
    SignupRequest,
    LoginRequest,
    UserResponse,
    TokenResponse,
    signup,
    login
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup_endpoint(
    signup_data: SignupRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.

    - **email**: User email address (must be unique)
    - **password**: User password (minimum 8 characters)
    - **name**: User display name

    Returns an access token and user data.
    Token should be included in Authorization header as: Bearer <token>
    """
    return await signup(db, signup_data)

@router.post("/login", response_model=TokenResponse)
async def login_endpoint(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.

    - **email**: User email address
    - **password**: User password

    Returns an access token and user data.
    Token should be included in Authorization header as: Bearer <token>
    """
    return await login(db, login_data)

@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information.

    Requires a valid JWT token in the Authorization header.
    Returns the user's profile information.
    """
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name
    )
