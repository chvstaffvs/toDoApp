from fastapi import APIRouter
from routes import (
    user,
    auth,
)

router = APIRouter()

router.include_router(auth.router, tags=["Autenticação"])
router.include_router(user.router, prefix="/user", tags=["Usuários"])
