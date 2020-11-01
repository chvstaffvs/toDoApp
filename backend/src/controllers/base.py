from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar

from pony import orm
from pony.orm.core import ObjectNotFound, TransactionIntegrityError
from models.database import db
from dtos.base import BaseDTO
from fastapi import HTTPException

from models.user import User


class BaseController(metaclass=ABCMeta):

    model: db.Entity
    dto: BaseDTO

    @classmethod
    @orm.db_session
    def create(cls, schema: dict, raw: bool = False):
        try:
            obj = cls.model(**schema)
            return obj if raw else cls.dto.parse_obj(obj.to_dict())
        except TransactionIntegrityError:
            raise HTTPException(400, detail="username already taken")

    @classmethod
    @orm.db_session
    def get(cls, id: int, raw: bool = False):
        try:
            obj = cls.model[id]
            return obj if raw else cls.dto.parse_obj(obj.to_dict())
        except ValueError:
            raise HTTPException(400, "Invalid id")
        except ObjectNotFound:
            raise HTTPException(404, detail="object not found")

    @classmethod
    @orm.db_session
    def get_by_field(cls, field: str, value: Any, raw: bool = False):
        obj = cls.model.get(**{field: value})
        if not obj:
            raise HTTPException(404, detail="object not found")
        return obj if raw else cls.dto.parse_obj(obj.to_dict())

    @classmethod
    @orm.db_session
    def list(cls, filters: dict = {}):
        query = cls.model.select()
        filtered_query = [
            item
            for item in query
            if all(getattr(item, f, None) == filters[f] for f in filters)
        ]
        return [cls.dto.parse_obj(obj.to_dict()) for obj in filtered_query]

    @classmethod
    @orm.db_session
    def update(cls, id: int, schema: dict):
        obj = cls.get(id, raw=True)
        obj.set(**{key: value for key, value in schema.items() if value is not None})
        return cls.dto.parse_obj(obj.to_dict())

    @classmethod
    @orm.db_session
    def delete(cls, id: int):
        obj = cls.get(id, raw=True)
        obj.delete()

    @classmethod
    @orm.db_session
    def protected_operation(cls, operation: str, id: int, user: User, *args, **kwargs):
        try:
            obj = cls.get(id, True)
            assert obj.user.id == user.id
            return getattr(cls, operation)(id, *args, **kwargs)
        except AssertionError:
            raise HTTPException(403, detail="todo not owned by user")