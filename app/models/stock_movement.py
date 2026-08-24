from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    product_id = Column(
        "product_id",
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    user_id = Column(
        "user_id",
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    movement_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    stock_before = Column(Integer, nullable=False)
    stock_after = Column(Integer, nullable=False)
    observation = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    product = relationship("Product")
    user = relationship("User")