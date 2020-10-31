from backend.src.settings import BASE_DIR
from pony.orm.core import Database

db = Database()

db.bind(provider="sqlite", filename=str(BASE_DIR / "db.sqlite3"), create_db=True)
