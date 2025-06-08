from pydantic import BaseModel, Field


class SRegistration(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)
    repeat_password: str = Field(min_length=8)


class SLogin(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)
