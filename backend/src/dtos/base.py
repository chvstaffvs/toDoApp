from re import S
from typing import Optional
from pydantic import BaseModel, create_model
import re
from pydantic.main import ModelMetaclass
from pydantic.fields import Field, ModelField


class MetaDTO(ModelMetaclass):
    @property
    def EditSchema(cls):
        fields = {**cls.__fields__}
        for name, model_field in fields.items():
            if isinstance(model_field, ModelField):
                fields[name] = (Optional[model_field.type_], Field(None))
        return create_model(
            cls.__name__.replace("DTO", "EditDTO"),
            __base__=cls,
            **fields,
        )


class BaseDTO(BaseModel, metaclass=MetaDTO):
    class Config:

        orm_mode = True
        allow_population_by_field_name = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            return re.sub("_([a-zA-Z])", lambda char: char[1].upper(), string)
