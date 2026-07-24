from pydantic import BaseModel
from typing import Optional, List

class CreateAccountSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config():
        from_attributes=True