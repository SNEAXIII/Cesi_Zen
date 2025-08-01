import pytest

from src.services.PasswordService import PasswordService
from src.security.secrets import SECRET
from tests.unit.service.mocks.password_mock import get_verify_mock, get_hash_mock
from tests.utils.utils_constant import HASHED_PASSWORD, PLAIN_PASSWORD


@pytest.mark.asyncio
async def test_good_password_verify(mocker):
    # Arrange
    mock_verify = get_verify_mock(mocker)
    mock_verify.return_value = True

    # Act
    result = await PasswordService.verify_password(PLAIN_PASSWORD, HASHED_PASSWORD)

    # Assert
    mock_verify.assert_called_once_with(PLAIN_PASSWORD, HASHED_PASSWORD)
    assert result is mock_verify.return_value


@pytest.mark.asyncio
async def test_wrong_password_verify(mocker):
    # Arrange
    mock_verify = get_verify_mock(mocker)
    mock_verify.return_value = False

    # Act
    result = await PasswordService.verify_password(PLAIN_PASSWORD, HASHED_PASSWORD)

    # Assert
    mock_verify.assert_called_once_with(PLAIN_PASSWORD, HASHED_PASSWORD)
    assert result is mock_verify.return_value


@pytest.mark.asyncio
async def test_password_hash(mocker):
    # Arrange
    mock_hash = get_hash_mock(mocker)
    mock_hash.return_value = HASHED_PASSWORD

    # Act
    result = await PasswordService.get_string_hash(PLAIN_PASSWORD)

    # Assert
    mock_hash.assert_called_once_with(PLAIN_PASSWORD, rounds=SECRET.BCRYPT_HASH_ROUND)
    assert result is mock_hash.return_value
