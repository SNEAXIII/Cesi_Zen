import uuid
from typing import Type

from pydantic import BaseModel
from httpx import Response


def is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except (ValueError, TypeError):
        return False


def extract_body_to_model(response: Response, model: Type[BaseModel]) -> BaseModel:
    return model.model_validate(response)
