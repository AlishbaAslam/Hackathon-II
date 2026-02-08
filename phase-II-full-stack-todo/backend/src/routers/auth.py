"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
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
