from fastapi import Depends
from fastapi.param_functions import Body
from routes.base import CustomRouter
from dtos.token import Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from controllers.auth import AuthController

router = CustomRouter()


@router.post("/token", response_model=Token)
async def authenticate(user_data: OAuth2PasswordRequestForm = Depends()):
    return AuthController.authenticate(user_data.username, user_data.password)


@router.post("/refresh", response_model=Token)
async def refresh_token(token: str = Body(..., embed=True)):
    return AuthController.refresh_token(token)
