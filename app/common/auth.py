from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class ResetPassword(BaseModel):
    email: str
    current_password: str
    new_password: str
