from .registry import mapper_registry
from sqlalchemy import Column, Integer, String, Boolean

@mapper_registry.mapped
class User:
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)

    def __repr__(self):
        return f"User({self.username}, {self.email})"