from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .movie import Movie

class Genre(SQLModel, table=True):
    id_genre: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)

    movies: List["Movie"] = Relationship(back_populates="genres", link_model="MovieGenre")