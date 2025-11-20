from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from .review import Review
    from .watchlist import Watchlist

class User(SQLModel, table=True):
    id_user: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    created_at: date = Field(default_factory=date.utcnow, nullable=False)

    reviews: List["Review"] = Relationship(back_populates="user")
    watchlist_user: List["Watchlist"] = Relationship(back_populates="user")

# SQLModel é a base 
# Field serve para declarar chave estrangeira e chave primária 
# Relationship serve para criar relacionamento entre classes
# Optional/List tipagem dos campos relacionais