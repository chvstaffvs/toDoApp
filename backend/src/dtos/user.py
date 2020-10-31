from dtos.base import BaseDTO
from datetime import date


class UserDTO(BaseDTO):
    username: str
    email: str
    first_name: str
    last_name: str
    birth_date: date


class RegisterUserDTO(UserDTO):
    password: str


class ResponseUserDTO(UserDTO):
    id: int
