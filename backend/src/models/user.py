from pony import orm
from models.database import db
from datetime import date
from passlib.hash import bcrypt

from models.todos import ToDos


class User(db.Entity):
    _table_ = "users"

    username = orm.Required(str, unique=True)
    password = orm.Required(str)
    email = orm.Required(str)
    first_name = orm.Required(str)
    last_name = orm.Required(str)
    birth_date = orm.Required(date)
    todos = orm.Set(ToDos, cascade_delete=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @orm.db_session
    def change_password(self):
        self.password = bcrypt.hash(self.password)

    def before_insert(self):
        self.change_password()

    @orm.db_session
    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password)
