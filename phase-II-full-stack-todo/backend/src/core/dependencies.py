"""
FastAPI dependencies for authentication and database access.
"""
from typing import Optional
from uuid import uuid4
import re
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.core.database import get_db
from src.core.security import verify_token
from src.core.jwt_middleware import get_current_user_from_better_auth, verify_better_auth_token
from src.models.user import User

# HTTP Bearer token security scheme
security = HTTPBearer()

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency that extracts and validates the current authenticated user from JWT token.
    Supports both custom JWT tokens and Better Auth tokens.

    Args:
        request: FastAPI request object
        db: Database session

    Returns:
        The authenticated User object

    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[len("Bearer "):]

    # Check if token is empty or undefined
    if not token or token == 'undefined' or token.strip() == '':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # First, try to verify as Better Auth token
    better_auth_payload = verify_better_auth_token(token)
    if better_auth_payload is not None:
        # Extract user information from Better Auth token
        better_auth_user_id = better_auth_payload.get("id") or better_auth_payload.get("sub")
        better_auth_email = better_auth_payload.get("email")
        better_auth_name = better_auth_payload.get("name", "User")

        if better_auth_user_id and better_auth_email:
            # Check if user exists in backend database
            result = await db.execute(select(User).where(User.email == better_auth_email))
            user = result.scalar_one_or_none()

            if user is None:
                # User doesn't exist in backend database, create them
                # Use the better_auth_user_id if it's a valid UUID format, otherwise generate a new one
                uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)

                if isinstance(better_auth_user_id, str) and uuid_pattern.match(better_auth_user_id):
                    # Use the Better Auth user ID if it's a valid UUID
                    new_user_id = better_auth_user_id
                else:
                    # Generate a new UUID for the backend
                    new_user_id = str(uuid4())

                user = User(
                    id=new_user_id,
                    email=better_auth_email,
                    name=better_auth_name
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)

            return user
        else:
            # Better Auth token is valid but missing required fields
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format - missing required fields",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # If Better Auth token verification failed, try custom JWT
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from custom token
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from database - convert string user_id to UUID for comparison
    from uuid import UUID
    try:
        user_uuid = UUID(user_id)
        result = await db.execute(select(User).where(User.id == user_uuid))
        user = result.scalar_one_or_none()
    except ValueError:
        # If user_id is not a valid UUID, the token is invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
