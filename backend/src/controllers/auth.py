from datetime import datetime, timedelta
from typing import Tuple
from fastapi import HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from controllers.user import UserController
from dtos.token import Token
from models.user import User
from jwt import PyJWTError, decode, encode

from settings import PROJECT_KEY

oauth_scheme = OAuth2PasswordBearer("/token")


class AuthController:
    @classmethod
    def token_exception(cls):
        raise HTTPException(400, detail="Invalid or expired token")

    @classmethod
    def verify_user(cls, user: User, password: str):
        if not user.verify_password(password):
            raise HTTPException(401, detail="password does not match")

    @classmethod
    def generate_token(cls, id: int, refresh: bool = False):
        data = {
            "sub": id,
            "exp": (
                datetime.utcnow()
                + (timedelta(minutes=15) if not refresh else timedelta(days=45))
            ),
            "refresh": refresh,
        }
        return encode(data, key=PROJECT_KEY, algorithm="HS512")

    @classmethod
    def authenticate(cls, username: str, password: str):
        user = UserController.get_by_username(username, True)
        cls.verify_user(user, password)
        return Token(
            access_token=cls.generate_token(user.id),
            refresh_token=cls.generate_token(user.id, True),
        )

    @classmethod
    def scan_token(cls, token: str) -> Tuple[User, bool]:
        try:
            data = decode(token, PROJECT_KEY, algorithms=["HS512"])
            user_id = data.get("sub")
            refresh = data.get("refresh")
            assert user_id
            assert refresh is not None
            return UserController.get(user_id, True), refresh
        except PyJWTError:
            cls.token_exception()
        except AssertionError:
            cls.token_exception()

    @classmethod
    def verify_token(cls, token: str = Depends(oauth_scheme)):
        try:
            user, refresh = cls.scan_token(token)
            assert not refresh
            return user
        except AssertionError:
            cls.token_exception()

    @classmethod
    def refresh_token(cls, token: str):
        try:
            user, refresh = cls.scan_token(token)
            assert refresh
            return Token(
                access_token=cls.generate_token(user.id),
                refresh_token=cls.generate_token(user.id, True),
            )
        except AssertionError:
            cls.token_exception()