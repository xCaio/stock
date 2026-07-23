from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import timezone, timedelta

db = create_engine("sqlite:///banco.db")
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name", String)
    email = Column("email", String, unique=True)
    password = Column("password", String)
    role = Column("role",String, default="user")

    def __init__(self, name, email, password, role="user"):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

class Product(Base):
    __tablename__ = "products"
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    code = Column("code", String, unique=True, nullable=False)
    product_type = Column("product_type", String, nullable=False)
    stock = Column("stock", Integer, default=0)
    stock_minimum = Column("stock_minimum", Integer, default=0)
    created_at =Column("created_at", DateTime, default=timezone.utc)
    updated_at = Column("updated_at", DateTime, default=timezone.utc, onupdate=timezone.utc)
    active = Column("active", Boolean, default=True)

    def __init__(self, code, product_type, stock, stock_minimum):
        self.code = code
        self.product_type = product_type
        self.stock = stock
        self.stock_minimum = stock_minimum
