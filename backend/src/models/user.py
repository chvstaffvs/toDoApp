from pony import orm
from models.database import db
from datetime import date
from passlib.hash import bcrypt


class User(db.Entity):
    _table_ = "users"

    username = orm.Required(str)
    password = orm.Required(str)
    email = orm.Required(str)
    first_name = orm.Required(str)
    last_name = orm.Required(str)
    birth_date = orm.Required(date)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @orm.db_session
    def change_password(self):
        self.password = bcrypt.hash(self.password)

    def before_insert(self):
        self.change_password()
