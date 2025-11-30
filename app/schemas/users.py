from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class UserBase(SQLModel):
    username: str
    email: str
    password: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id_user: int
    created_at: datetime


class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
