# tests/conftest.py

import asyncio
import pytest
import pytest_asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.models import Base
from app.db.session import get_db
from app.main import app

# 1) event loop for pytest-asyncio
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# 2) expose FastAPI app
@pytest.fixture(scope="session")
def test_app():
    return app

# 3) test database setup/teardown
TEST_DATABASE_URL = str(settings.DATABASE_URL).replace(f"/{settings.POSTGRES_DB}", "/test_db")
_engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
_TestingSessionLocal = sessionmaker(_engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session")
async def test_db_setup():
    async with _engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with _engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# 4) provide a clean AsyncSession per test
@pytest_asyncio.fixture
async def db_session(test_db_setup) -> AsyncSession:
    async with _TestingSessionLocal() as session:
        yield session
        await session.rollback()

# 5) HTTPX AsyncClient
@pytest_asyncio.fixture
async def client(test_app) -> AsyncClient:
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac

# 6) mocks for external calls
@pytest.fixture
def mock_openai_response(monkeypatch):
    async def _mock_clean(a, b):
        return {"source": "Toronto", "destination": "Vancouver",
                "sourceCorrected": False, "destinationCorrected": False}
    from app.services import address_cleaner
    monkeypatch.setattr(address_cleaner, "clean_addresses", _mock_clean)

@pytest.fixture
def mock_recaptcha_verify(monkeypatch):
    async def _mock_verify(token: str):
        # do nothing / no exception = success
        return None

    # patch the service itself
    from app.services import recaptcha
    monkeypatch.setattr(recaptcha, "verify_recaptcha", _mock_verify)

    # patch the imported name in your router module
    import app.api.distance as dist_mod
    monkeypatch.setattr(dist_mod, "verify_recaptcha", _mock_verify)

@pytest.fixture
def mock_nominatim_response(monkeypatch):
    async def _mock_geo(address: str, address_type: str):
        if address_type == "source":
            return (43.6532, -79.3832)
        return (49.2827, -123.1207)
    from app.services import geocode
    monkeypatch.setattr(geocode, "get_coordinates", _mock_geo)
