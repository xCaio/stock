from sqlalchemy import Column, Integer, String

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name", String)
    email = Column("email", String, unique=True)
    password = Column("password", String)
    role = Column("role", String, default="user")

    def __init__(self, name, email, password, role="user"):
        self.name = name
        self.email = email
        self.password = password
        self.role = role