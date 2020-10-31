from pydantic.main import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: int = 900