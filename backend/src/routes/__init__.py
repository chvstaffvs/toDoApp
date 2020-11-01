from fastapi import APIRouter
from routes import (
    user,
    auth,
    todos,
)

router = APIRouter()

router.include_router(auth.router, tags=["Autenticação"])
router.include_router(user.router, prefix="/user", tags=["Usuários"])
router.include_router(todos.router, prefix="/todo", tags=["Tarefas"])