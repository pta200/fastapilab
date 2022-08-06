from uuid import UUID
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    item_id: UUID
    user_id: UUID

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    user_name: str


class User(UserBase):
    user_id: UUID
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
