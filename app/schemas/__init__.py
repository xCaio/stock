from app.schemas.auth import CreateAccountSchema, LoginSchema

from app.schemas.product import (
    SuppliesSchema,
    ProductResponseSchema,
    ProductUpdateSchema,
    ProductAdjustmentSchema,
)

from app.schemas.stock_movement import (
    StockMovementSchema,
    MovementSchema,
    StockMovementResponse,
)

from app.schemas.user import (
    UserUpdateSchema,
    UserRoleSchema,
)