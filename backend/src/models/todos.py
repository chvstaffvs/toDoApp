from datetime import date
from models.database import db
from pony import orm


class ToDos(db.Entity):
    _table_ = "todos"

    name = orm.Required(str)
    description = orm.Optional(orm.LongStr)
    done = orm.Required(bool, default=False)
    user = orm.Required("User")
    expected_date = orm.Optional(date)
    active = orm.Required(bool, default=False)
