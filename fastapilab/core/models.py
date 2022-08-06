from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import uuid


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    user_name = Column(String)
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="user")


class Item(Base):
    __tablename__ = "items"
    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    user = relationship("User", back_populates="items")
