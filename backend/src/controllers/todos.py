from fastapi.exceptions import HTTPException
from pony import orm
from controllers.base import BaseController
from models import ToDos, User
from dtos.todos import ToDosResponseDTO


class ToDosController(BaseController):

    model = ToDos
    dto = ToDosResponseDTO

    @classmethod
    @orm.db_session
    def get_from_user(cls, user: User, filters: dict = {}):
        query = user.todos.select()
        return (
            cls.dto.parse_obj(item.to_dict())
            for item in query
            if all(getattr(item, key) == value for key, value in filters.items())
        )

    @classmethod
    @orm.db_session
    def create(cls, schema: dict, user: User, raw: bool = False):
        schema["user"] = user.id
        return super().create(schema, raw)

    @classmethod
    @orm.db_session
    def wipe(cls, user: User):
        user.todos.clear()
