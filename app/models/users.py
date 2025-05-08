import re
from typing import Annotated, Optional
from bson import ObjectId
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string"}

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values=None, field=None):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


# Shared base user schema
class UserBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    firstName: str = Field(..., min_length=2)
    lastName: str = Field(..., min_length=2)
    email: EmailStr
    phone: str = Field(..., min_length=10)
    password: str = Field(..., min_length=8)

    @field_validator("password")
    def validate_password(cls, v):
        import re

        pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must contain at least one uppercase letter, one digit, and one special character."
            )
        return v

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        schema_extra={
            "example": {
                "firstName": "Romesh",
                "lastName": "Langoljam",
                "email": "romesh@yopmail.com",
                "phone": "9565656556",
                "password": "Password@1",
            }
        },
    )


class UpdateUserSchema(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    password: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "firstName": "UpdatedName",
                "email": "updated@example.com",
                "phone": "9999999999",
            }
        }


class UserResponse(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr

    model_config = ConfigDict(
        schema_extra={
            "example": {
                "firstName": "Romesh",
                "lastName": "Langoljam",
                "email": "romesh@yopmail.com",
            }
        }
    )
