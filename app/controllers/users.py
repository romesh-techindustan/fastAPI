from fastapi import APIRouter

from app.services.users import GetAllUsers, GetDetails

router = APIRouter()


@router.get("/{id}", response_description="Get user details")
async def get_user(id):
    return await GetDetails(id)


@router.get("/", response_description="List all users")
async def get_all_users():
    users = await GetAllUsers()
    return users


# @router.get("/{id}", response_description="Get a single user")
# async def get_user(id: str):
#     user = await retrieve_user(id)
#     if user:
#         return user
#     raise HTTPException(status_code=404, detail="User not found")


# @router.patch("/{id}", response_description="Update a user")
# async def patch_user(id: str, data: UpdateUserSchema):
#     updated = await update_user(id, data.dict(exclude_unset=True))
#     if updated:
#         return {"message": "User updated successfully"}
#     raise HTTPException(status_code=404, detail="User not found or no changes applied")


# @router.delete("/{id}", response_description="Delete a user")
# async def remove_user(id: str):
#     deleted = await delete_user(id)
#     if deleted:
#         return {"message": "User deleted successfully"}
#     raise HTTPException(status_code=404, detail="User not found")
