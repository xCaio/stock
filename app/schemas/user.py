from typing import Optional, Literal

from pydantic import BaseModel, EmailStr


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True


class UserRoleSchema(BaseModel):
    role: Literal["user", "admin"]

    class Config:
        from_attributes = True