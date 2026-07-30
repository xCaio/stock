from datetime import datetime, timezone

from pydantic import BaseModel, field_validator, EmailStr, ConfigDict, field_serializer
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

class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    movement_type: str
    quantity: int
    stock_before: int
    stock_after: int
    observation: str | None = None
    created_at: datetime
    user_name: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    @classmethod
    def from_movement(cls, movement) -> "StockMovementResponse":
        return cls(
            id=movement.id,
            product_id=movement.product_id,
            user_id=movement.user_id,
            movement_type=movement.movement_type,
            quantity=movement.quantity,
            stock_before=movement.stock_before,
            stock_after=movement.stock_after,
            observation=movement.observation,
            created_at=movement.created_at,
            user_name=movement.user.name if movement.user else None,
        )

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
