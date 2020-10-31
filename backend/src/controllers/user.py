from pony import orm
from controllers.base import BaseController
from models import User
from dtos import ResponseUserDTO
from fastapi import HTTPException


class UserController(BaseController):

    model = User
    dto = ResponseUserDTO

    @classmethod
    @orm.db_session
    def get_by_username(cls, username: str, raw: bool = False):
        return cls.get_by_field("username", username, raw)

    @classmethod
    @orm.db_session
    def get_by_email(cls, email: str, raw: bool = False):
        return cls.get_by_field("email", email, raw)

    @classmethod
    @orm.db_session
    def change_password(cls, id: int, password: str):
        user = cls.get(id, raw=True)
        user.password = password
        user.change_password()
        return cls.dto.from_orm(user)