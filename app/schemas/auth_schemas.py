from pydantic import EmailStr
from pydantic import BaseModel


class RequestLoginSchema(BaseModel):
    username: EmailStr
    password: str


class ResponseLoginSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
