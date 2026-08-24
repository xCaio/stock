from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator

from app.enums.types import MovementType


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
    def normalize_movement_type(cls, value):
        return value.lower()

    class Config:
        from_attributes = True


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