from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    code = Column("code", String, unique=True, nullable=False)
    product_type = Column("product_type", String, nullable=False)
    stock = Column("stock", Integer, default=0)
    stock_minimum = Column("stock_minimum", Integer, default=0)
    created_at = Column(
        "created_at",
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    active = Column("active", Boolean, default=True)

    def __init__(self, code, product_type, stock, stock_minimum):
        self.code = code
        self.product_type = product_type
        self.stock = stock
        self.stock_minimum = stock_minimum