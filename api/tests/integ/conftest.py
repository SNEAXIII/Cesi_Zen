import pytest

from main import app
from tests.utils.utils_db import reset_test_db, delete_db
from src.utils.db import get_session
from tests.utils.utils_db import get_test_session

app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(autouse=True, scope="function")
def call_reset_db():
    reset_test_db()

@pytest.fixture(scope="session", autouse=True)
def delete_test_db():
    delete_db()
    yield
    delete_db()

