from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .review import Review
    from .watchlist import Watchlist

class User(SQLModel, table=True):
    __tablename__ = "user"
    
    id_user: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False, index=True, max_length=50)
    email: str = Field(unique=True, nullable=False, index=True, max_length=255)
    password: str = Field(nullable=False, min_length=6)
    full_name: Optional[str] = Field(default=None, nullable=True, max_length=100)  # Adicionado
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_active: bool = Field(default=True, nullable=False)  # Adicionado

    # Relações
    reviews: List["Review"] = Relationship(back_populates="user")
    watchlists: List["Watchlist"] = Relationship(back_populates="user")