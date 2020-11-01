from pydantic.fields import Field
from dtos.base import BaseDTO
from datetime import date
from typing import Optional


class ToDosDTO(BaseDTO):
    name: str
    description: str = Field("")
    done: bool
    expected_date: Optional[date] = Field(None)
    active: bool


class ToDosResponseDTO(ToDosDTO):
    id: int