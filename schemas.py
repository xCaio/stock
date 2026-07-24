from pydantic import BaseModel
from typing import Optional, List

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

    class Config():
        from_attributes = True

class ProductResponseSchema(BaseModel):
    id: int
    code: str
    product_type: str
    stock: int

    class Config():
        from_attributes = True
