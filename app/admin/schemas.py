from typing import Optional

from pydantic import BaseModel, Field


class SPost(BaseModel):
    header: str
    text: str


class SUpdatePost(BaseModel):
    header: Optional[str | None] = Field(min_length=1)
    text: Optional[str | None] = Field(min_length=1)
