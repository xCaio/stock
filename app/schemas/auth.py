from pydantic import BaseModel, EmailStr


class CreateAccountSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True