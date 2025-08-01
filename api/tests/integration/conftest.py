
import pytest_asyncio
import pytest

from main import app
from tests.utils.utils_db import reset_test_db, delete_db, Session
from src.utils.db import get_session
from tests.utils.utils_db import get_test_session


@pytest.fixture(autouse=True, scope="function")
def reset_db() -> None:
    # Setup
    reset_test_db()
    app.dependency_overrides[get_session] = get_test_session

    # Test
    yield

    # Teardown
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def session():
    async with Session() as session:
        yield session

@pytest.fixture(scope="session", autouse=True)
def delete_test_db():
    delete_db()
    yield
    delete_db()
