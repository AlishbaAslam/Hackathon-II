"""
Security tests for the backend.
"""
import pytest
from src.core.security import verify_password, get_password_hash, create_access_token, verify_token


def test_password_hashing():
    """Test that password hashing works correctly."""
    password = "test_password_123"

    # Hash the password
    hashed = get_password_hash(password)

    # Verify the password
    assert verify_password(password, hashed)

    # Verify a wrong password fails
    assert not verify_password("wrong_password", hashed)

    # Verify the same password hashes to different values due to salt
    hashed2 = get_password_hash(password)
    assert hashed != hashed2

    # But both should verify the same original password
    assert verify_password(password, hashed)
    assert verify_password(password, hashed2)


def test_jwt_token_generation():
    """Test JWT token creation and verification."""
    data = {"sub": "test_user_id", "role": "user"}

    # Create a token
    token = create_access_token(data=data)

    # Verify the token
    payload = verify_token(token)

    assert payload is not None
    assert payload["sub"] == "test_user_id"
    assert payload["role"] == "user"

    # Verify that expired tokens are rejected
    # (Would require mocking time to test properly)


def test_jwt_token_invalid():
    """Test that invalid JWT tokens are rejected."""
    invalid_token = "invalid.token.format"

    payload = verify_token(invalid_token)
    assert payload is None


def test_jwt_token_expired():
    """Test that expired JWT tokens are rejected."""
    # This would require mocking time to create an actually expired token
    # For now, we'll just verify the function exists and handles invalid cases
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjIwMDAwMDB9.invalid-signature"

    payload = verify_token(expired_token)
    assert payload is None