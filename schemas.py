from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional, Literal
from enums import MovementType

ALLOWED_PRODUCT_TYPES = ("etiqueta", "ribbon")


def normalize_product_type_value(value: str) -> str:
    normalized = str(value).strip().lower()
    if normalized in ("etiqueta", "etiquetas"):
        return "etiqueta"
    if normalized in ("ribbon", "ribbons"):
        return "ribbon"
    raise ValueError('product_type deve ser "etiqueta" ou "ribbon"')


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
    product_type: Literal["etiqueta", "ribbon"]
    stock: int
    stock_minimum: int

    @field_validator("product_type", mode="before")
    @classmethod
    def normalize_product_type(cls, value):
        return normalize_product_type_value(value)

    @field_validator("code")
    @classmethod
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
    product_type: Literal["etiqueta", "ribbon"]

    @field_validator("product_type", mode="before")
    @classmethod
    def normalize_product_type(cls, value):
        return normalize_product_type_value(value)

    @field_validator("code")
    @classmethod
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
    @classmethod
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

class UserRoleSchema(BaseModel):
    role: Literal["user", "admin"]

    class Config():
            from_attributes=True

class ProductAdjustmentSchema(BaseModel):
    new_stock: int
    reason: str

    class Config():
            from_attributes=True
