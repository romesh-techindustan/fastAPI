from http.client import HTTPException
from bson import ObjectId
from app.models.users import UserResponse
from app.connections.db import user_collection
from app.common.response import Response

from bson import ObjectId
from fastapi.responses import JSONResponse


async def GetDetails(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})

    if user:
        user = UserResponse(**user)
        return Response(user, "Get user details")
    else:
        return JSONResponse(status_code=404, content={"message": "User not found"})


async def GetAllUsers():
    users_cursor = user_collection.find()
    users = []
    for user in await users_cursor.to_list(length=100):
        user["_id"] = str(user["_id"])
        users.append(UserResponse(**user))
    if not users:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    return Response(users, "Get all users successfully.")


async def get_user_by_email(email: str):
    user = await user_collection.find_one({"email": email})

    if not user:
        return
    return user
