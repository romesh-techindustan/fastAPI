from bson import ObjectId
from .users import get_user_by_email
from app.common.response import Response
from app.models.users import UserResponse
from passlib.hash import pbkdf2_sha256
from app.connections.db import user_collection


async def SignUp(user_dict: dict):
    try:
        user_dict["password"] = pbkdf2_sha256.hash(user_dict["password"])
        user_dict["_id"] = ObjectId()
        await user_collection.insert_one(user_dict)
        user_dict["_id"] = str(user_dict["_id"])
        return Response(UserResponse(**user_dict), "Get users")
    except Exception as e:
        raise Exception(f"Error inserting user: {str(e)}")


async def login(login: dict):
    try:
        user = await get_user_by_email(login["email"])
        if user and pbkdf2_sha256.verify(login["password"], user["password"]):
            user["_id"] = str(user["_id"])
            return Response(UserResponse(**user), "Login successfull.")
        else:
            return Response(None, "Invalid credentials!")
    except Exception as e:
        print(e)
        raise Exception(f"Invalid credentials!")


async def reset_password(login: dict):
    try:
        user = await get_user_by_email(login["email"])
        if user and pbkdf2_sha256.verify(login["current_password"], user["password"]):
            user["password"] = pbkdf2_sha256.hash(login["new_password"])
            await user_collection.update_one(
                ObjectId(user["_id"]), {"password": user["password"]}
            )
            user["_id"] = str(user["_id"])
            return Response(UserResponse(**user), "Rest password successfully.")
        else:
            return Response(None, "Invalid credentials!")
    except Exception as e:
        print(e)
        raise Exception(f"Invalid credentials!")
