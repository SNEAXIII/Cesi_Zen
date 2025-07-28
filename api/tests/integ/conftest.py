import pytest

from main import app
from tests.utils.utils_db import reset_test_db, delete_db
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


# @pytest.fixture()
# async def session() -> None:
#     async with get_test_session_maker() as session:
#         yield session


@pytest.fixture(scope="session", autouse=True)
def delete_test_db():
    delete_db()
    yield
    delete_db()
