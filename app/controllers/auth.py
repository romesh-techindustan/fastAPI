from fastapi import APIRouter
from app.common.auth import Login, ResetPassword
from app.models.users import UserBase
from app.services.auth import login, reset_password, SignUp


router = APIRouter()


@router.post("/sign-up", response_description="Create new user")
async def create_user(request: UserBase):
    user_dict = request.dict(by_alias=True)
    user = await SignUp(user_dict)
    return user


@router.post("/login", response_description="Login")
async def login_route(request: Login):
    user_dict = request.dict(by_alias=True)
    user = await login(user_dict)
    return user


@router.post("/reset-password", response_description="Reset password")
async def password_reset(request: ResetPassword):
    user_dict = request.dict(by_alias=True)
    return await reset_password(user_dict)
