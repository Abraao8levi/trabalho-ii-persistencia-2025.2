from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .movie import Movie

class Actor(SQLModel, table=True):
    id_actor: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    birth_date: Optional[str] = Field(default=None, nullable=True)
    nationality: Optional[str] = Field(default=None, nullable=True)
    biography: Optional[str] = Field(default=None, nullable=True)

    movies: List["Movie"] = Relationship(back_populates="actors", link_model="MovieActor")