"""
JWT Middleware for verifying Better Auth tokens in FastAPI

Supports both symmetric (HS256) and asymmetric (RS256, ES256) JWT verification.
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Request
from fastapi.security.http import HTTPBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from src.config import settings

# HTTP Bearer token security scheme
security = HTTPBearer()


def verify_better_auth_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a Better Auth JWT token.

    Supports multiple verification strategies:
    1. HS256 with BETTER_AUTH_SECRET (symmetric)
    2. HS256 with SECRET_KEY (fallback)
    3. RS256/ES256 with JWKS (asymmetric - if JWKS_URL is configured)

    Args:
        token: The JWT token to verify

    Returns:
        Decoded token payload if valid, None if invalid or expired
    """
    # Strategies for token verification in order of preference
    verification_strategies = []

    # Strategy 1: Try BETTER_AUTH_SECRET with HS256
    if settings.BETTER_AUTH_SECRET:
        verification_strategies.append({
            "secret": settings.BETTER_AUTH_SECRET,
            "algorithms": ["HS256"]
        })

    # Strategy 2: Try SECRET_KEY with configured algorithm (fallback)
    if settings.SECRET_KEY and settings.SECRET_KEY != settings.BETTER_AUTH_SECRET:
        verification_strategies.append({
            "secret": settings.SECRET_KEY,
            "algorithms": [settings.ALGORITHM]
        })

    # Strategy 3: Try JWKS for asymmetric algorithms (RS256, ES256)
    if hasattr(settings, 'JWKS_URL') and settings.JWKS_URL:
        verification_strategies.append({
            "jwks_url": settings.JWKS_URL,
            "algorithms": ["RS256", "ES256"]
        })

    # Try each strategy
    for strategy in verification_strategies:
        try:
            if "jwks_url" in strategy:
                # Asymmetric verification using JWKS
                jwks_client = jwt.JWT.JWK(requests_cache=False)
                jwks_client = jwt.JWT.jwk_cache(strategy["jwks_url"])
                payload = jwt.decode(
                    token,
                    jwks_client,
                    algorithms=strategy["algorithms"],
                    options={"verify_aud": False}
                )
            else:
                # Symmetric verification using secret
                payload = jwt.decode(
                    token,
                    strategy["secret"],
                    algorithms=strategy["algorithms"],
                    options={"verify_aud": False}
                )
            return payload
        except ExpiredSignatureError:
            # Don't try other strategies for expired tokens
            return None
        except JWTError:
            # Continue to next strategy
            continue

    return None


async def get_current_user_from_better_auth(request: Request) -> Dict[str, Any]:
    """
    Extract and validate the current authenticated user from Better Auth JWT token.

    Args:
        request: FastAPI request object

    Returns:
        The authenticated user data from the token

    Raises:
        HTTPException: 401 if token is invalid
    """
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[len("Bearer "):]

    # Verify and decode token
    payload = verify_better_auth_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user data from token (Better Auth typically has 'id' in the token)
    user_id = payload.get("id") or payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format - missing user id",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return user data
    return {
        "id": user_id,
        "email": payload.get("email"),
        "name": payload.get("name")
    }
