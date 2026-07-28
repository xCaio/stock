from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional, List
from enums import MovementType

class CreateAccountSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config():
        from_attributes=True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config():
        from_attributes = True

class SuppliesSchema(BaseModel):
    code: str
    product_type: str
    stock: int
    stock_minimum: int

    @field_validator("product_type")
    def normalize_product_type(cls, value):
        return value.lower()
    @field_validator("code")
    def normalize_code(cls, value):
        return value.upper()

    class Config():
        from_attributes = True

class ProductResponseSchema(BaseModel):
    id: int
    code: str
    product_type: str
    stock: int

    class Config():
        from_attributes = True

class ProductUpdateSchema(BaseModel):
    code: str
    product_type: str

    @field_validator("code")
    def normalize_code(cls, value):
        return value.upper()

    class Config():
        from_attributes=True

class StockMovementSchema(BaseModel):
    quantity: int
    observation: str | None = None

class MovementSchema(BaseModel):
    product_id: int
    movement_type: MovementType
    quantity: int
    observation: str | None = None

    @field_validator("movement_type", mode="before")
    def normalize_moviment_type(cls, value):
        return value.lower()

    class Config():
        from_attributes=True

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None

    class Config():
        from_attributes=True