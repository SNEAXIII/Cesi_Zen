from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    token_type: str = Field(examples=["bearer"])
    access_token: str = Field(examples=["access_token"])
