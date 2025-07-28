import re
from datetime import datetime, timezone, timedelta

import pytest
from httpx import Response

from src.Messages.validators_messages import VALIDATION_ERROR
from src.dto.dto_token import LoginResponse
from src.enums.Roles import Roles
from src.models import Article, Category, User, LoginLog, ExerciseCoherenceCardiac  # noqa: F401
from main import app
from src.security.secrets import SECRET
from src.services.JWTService import JWTService
from src.utils.db import get_session
from tests.integ.endpoints.setup.user_setup import push_one_user
from tests.utils.utils_constant import PLAIN_PASSWORD, USER_LOGIN, USER_ID, USER_EMAIL
from tests.utils.utils_db import get_test_session, reset_test_db
from tests.utils.utils_client import execute_post_request
from tests.utils.utils_random import extract_body_to_model

app.dependency_overrides[get_session] = get_test_session

# --- Constants ---
REGEX_BEARER = re.compile(r"(eyJ[\da-zA-Z]+\.){2}[\w-]+")
TOKEN_TYPE = "bearer"
ERROR_KEY = "errors"
PAYLOAD_KEY = "payload"
MISSING_TYPE = "missing"
MISSING_MESSAGE = "Field required"
USERNAME_KEY = "username"
PASSWORD_KEY = "password"


# --- Utility functions ---
def get_field_error(field: str, message: str, type: str) -> dict:
    return {field: {"message": message, "type": type}}


def get_field_missing_error(field: str) -> dict:
    """
    Sample of return value:
    {
        "field": {
            "message": "Field required",
            "type": "missing"
        }
    }
    """
    return get_field_error(field, MISSING_MESSAGE, MISSING_TYPE)


def login_bad_params(
    contains_username: bool = True, contains_password: bool = True
) -> dict:
    """
    Sample of return value for both variables = True:
    {
        "payload": {},
        "errors": {
            "message": "Erreur lors de la validation",
            "errors": {
                "username": {
                    "message": "Field required",
                    "type": "missing"
                },
                "password": {
                    "message": "Field required",
                    "type": "missing"
                }
            }
        }
    }
    """
    payload = {}
    expected_errors = {"message": VALIDATION_ERROR, ERROR_KEY: {}}
    fields = {"username": contains_username, "password": contains_password}
    for field, present in fields.items():
        if present:
            payload[field] = ""
        else:
            new_error = get_field_missing_error(field)
            expected_errors[ERROR_KEY].update(new_error)
    return {PAYLOAD_KEY: payload, ERROR_KEY: expected_errors}


async def login_request() -> Response:
    await push_one_user()
    payload = {USERNAME_KEY: USER_LOGIN, PASSWORD_KEY: PLAIN_PASSWORD}
    route = "/auth/login"
    return await execute_post_request(route, payload=payload)


async def success_login() -> LoginResponse:
    response = await login_request()
    return extract_body_to_model(response.json(), LoginResponse)  # type: ignore


# --- Test cases ---
params_login_bad_request = {
    "missing_password": login_bad_params(contains_username=False),
    "missing_password_params": login_bad_params(contains_password=False),
    "missing_everything_params": login_bad_params(
        contains_username=False, contains_password=False
    ),
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    params_login_bad_request.values(),
    ids=[f"case_{k}" for k in params_login_bad_request.keys()],
)
async def test_login_bad_request(values: dict):
    # Arrange
    route = "/auth/login"

    # Act
    response = await execute_post_request(route, payload=values[PAYLOAD_KEY])
    print(values)

    # Assert
    assert response.status_code == 400
    assert response.json() == values[ERROR_KEY]


@pytest.mark.asyncio
async def test_login_authorize_status_code():
    # Arrange & act
    response = await login_request()

    # Assert
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_authorize_token_type():
    # Arrange & act
    body = await success_login()

    # Assert
    assert body.token_type == TOKEN_TYPE


@pytest.mark.asyncio
async def test_login_authorize_token_format():
    # Arrange & act
    body = await success_login()

    # Assert
    token = body.access_token
    assert REGEX_BEARER.match(token), f"The token format is not valid: {token}"


@pytest.mark.asyncio
async def test_login_authorize_expiration_date(freezer):
    # Arrange & act
    body = await success_login()

    # Assert
    jwt_payload = JWTService.decode_jwt(body.access_token)
    expiration_td = timedelta(minutes=SECRET.ACCESS_TOKEN_EXPIRE_MINUTES)
    created_at = datetime.now(tz=timezone.utc).replace(microsecond=0)
    expected_time = (created_at + expiration_td).timestamp()
    assert jwt_payload["exp"] == expected_time


@pytest.mark.asyncio
async def test_login_authorize_user_id():
    # Arrange & act
    body = await success_login()

    # Assert
    jwt_payload = JWTService.decode_jwt(body.access_token)
    assert jwt_payload["user_id"] == str(USER_ID)


@pytest.mark.asyncio
async def test_login_authorize_sub():
    # Arrange & act
    body = await success_login()

    # Assert
    jwt_payload = JWTService.decode_jwt(body.access_token)
    assert jwt_payload["sub"] == USER_LOGIN


@pytest.mark.asyncio
async def test_login_authorize_email():
    # Arrange & act
    body = await success_login()

    # Assert
    jwt_payload = JWTService.decode_jwt(body.access_token)
    assert jwt_payload["email"] == USER_EMAIL


@pytest.mark.asyncio
async def test_login_authorize_role():
    # Arrange & act
    body = await success_login()

    # Assert
    jwt_payload = JWTService.decode_jwt(body.access_token)
    assert jwt_payload["role"] == Roles.USER
