"""
Authentication service logic for user signup and login.
"""
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status
from src.models.user import User
from src.core.security import verify_password, get_password_hash, create_access_token
from src.core.exceptions import ConflictException, UnauthorizedException

# Request/Response Schemas

from typing import Optional

class SignupRequest(BaseModel):
    """Request schema for user signup."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)  # bcrypt limit is 72 bytes
    name: Optional[str] = Field(default=None, max_length=100)

class LoginRequest(BaseModel):
    """Request schema for user login."""
    email: EmailStr
    password: str = Field(max_length=72)  # bcrypt limit is 72 bytes

class UserResponse(BaseModel):
    """Response schema for user data."""
    id: str
    email: str
    name: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Response schema for authentication token."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Service Functions

async def signup(db: AsyncSession, signup_data: SignupRequest) -> TokenResponse:
    """
    Create a new user account.

    Args:
        db: Database session
        signup_data: Signup request data

    Returns:
        TokenResponse with access token and user data

    Raises:
        HTTPException: 409 if email already exists
    """
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == signup_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ConflictException(detail="Email already exists")

    # Hash password
    hashed_password = get_password_hash(signup_data.password)

    # Create new user
    name = signup_data.name if signup_data.name else f"User_{signup_data.email.split('@')[0]}"
    new_user = User(
        email=signup_data.email,
        hashed_password=hashed_password,
        name=name
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Generate JWT token for the new user
    access_token = create_access_token(data={
        "sub": str(new_user.id),
        "email": new_user.email,
        "name": new_user.name
    })

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=str(new_user.id),
            email=new_user.email,
            name=new_user.name,
            created_at=new_user.created_at
        )
    )

async def login(db: AsyncSession, login_data: LoginRequest) -> TokenResponse:
    """
    Authenticate user and generate JWT token.

    Args:
        db: Database session
        login_data: Login request data

    Returns:
        TokenResponse with access token and user data

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Find user by email
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(login_data.password, user.hashed_password):
        raise UnauthorizedException(detail="Invalid email or password")

    # Generate JWT token with user info for Better Auth compatibility
    access_token = create_access_token(data={
        "sub": str(user.id),
        "email": user.email,
        "name": user.name
    })

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            created_at=user.created_at
        )
    )
