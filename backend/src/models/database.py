from pony.orm import Database
from settings import BASE_DIR

db = Database()

db.bind(provider="sqlite", filename=str(BASE_DIR / "db.sqlite3"), create_db=True)
