# tests/test_distance_api.py

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.db.session import get_db

pytestmark = pytest.mark.asyncio

# Hard-coded endpoint paths
DISTANCE_PATH = "/api/v1/distance"
HISTORY_PATH = "/api/v1/history"

async def override_get_db(db_session: AsyncSession):
    """
    Override FastAPI's get_db dependency to use our test session,
    and roll back at the end of each request.
    """
    async def _get_db():
        try:
            yield db_session
        finally:
            await db_session.rollback()
    app.dependency_overrides[get_db] = _get_db

async def clear_db_override():
    """Clear any dependency overrides."""
    app.dependency_overrides.clear()


async def test_calculate_distance_success(
    client: AsyncClient,
    db_session: AsyncSession,
    mock_openai_response,
    mock_recaptcha_verify,
    mock_nominatim_response
):
    """POST /api/v1/distance returns 200 and payload with kilometers & miles."""
    await override_get_db(db_session)
    try:
        response = await client.post(
            DISTANCE_PATH,
            json={
                "source": "Toronto, ON, Canada",
                "destination": "Vancouver, BC, Canada",
                "captchaToken": "test_token"
            }
        )
        assert response.status_code == 200

        data = response.json()
        # The route now returns 'kilometers' and 'miles'
        assert "kilometers" in data and "miles" in data
        assert isinstance(data["kilometers"], float)
        assert isinstance(data["miles"], float)

        # It also returns the cleaned addresses
        assert data["source_address"] == "Toronto, ON, Canada"
        assert data["destination_address"] == "Vancouver, BC, Canada"
    finally:
        await clear_db_override()


async def test_calculate_distance_invalid_input(
    client: AsyncClient,
    db_session: AsyncSession
):
    """Empty source should return 422 Unprocessable Entity."""
    await override_get_db(db_session)
    try:
        response = await client.post(
            DISTANCE_PATH,
            json={
                "source": "",
                "destination": "Vancouver, BC, Canada",
                "captchaToken": "test_token"
            }
        )
        assert response.status_code == 422
    finally:
        await clear_db_override()


async def test_calculate_distance_missing_captcha(
    client: AsyncClient,
    db_session: AsyncSession,
    mock_openai_response,
    mock_nominatim_response
):
    """Empty captchaToken should return 400 Bad Request."""
    await override_get_db(db_session)
    try:
        response = await client.post(
            DISTANCE_PATH,
            json={
                "source": "Toronto, ON, Canada",
                "destination": "Vancouver, BC, Canada",
                "captchaToken": ""
            }
        )
        assert response.status_code == 400
    finally:
        await clear_db_override()


async def test_distance_history(
    client: AsyncClient,
    db_session: AsyncSession,
    mock_recaptcha_verify
):
    """GET /api/v1/history returns a list with source, destination, kilometers, miles, created_at."""
    await override_get_db(db_session)
    try:
        # Create one history entry
        await client.post(
            DISTANCE_PATH,
            json={
                "source": "Toronto, ON, Canada",
                "destination": "Vancouver, BC, Canada",
                "captchaToken": "test_token"
            }
        )

        # Fetch history (note: uses GET + query param)
        response = await client.get(f"{HISTORY_PATH}?captchaToken=test_token")
        assert response.status_code == 200

        history = response.json()
        assert isinstance(history, list) and len(history) >= 1
        record = history[0]

        # Check that each expected field is present
        for key in (
            "source",
            "destination",
            "kilometers",
            "miles",
            "created_at"
        ):
            assert key in record
    finally:
        await clear_db_override()
