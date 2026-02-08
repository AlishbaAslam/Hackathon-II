"""
Documentation tests for the backend.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_docs_endpoint_accessible(client):
    """Test GET /docs returns 200."""
    response = await client.get("/docs")
    # The /docs endpoint returns HTML, so we expect 200 OK
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_redoc_endpoint_accessible(client):
    """Test GET /redoc returns 200."""
    response = await client.get("/redoc")
    # The /redoc endpoint returns HTML, so we expect 200 OK
    assert response.status_code == 200