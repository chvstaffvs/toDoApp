from models.database import db
from models.user import User
from models.todos import ToDos

db.generate_mapping(create_tables=True)