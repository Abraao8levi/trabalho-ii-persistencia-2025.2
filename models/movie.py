from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional
from datetime import date
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .review import Review
    from .watchlist import Watchlist
    from .genre import Genre
    from .actor import Actor

class Movie(SQLModel, table=True):
    __tablename__ = "movie"
    
    id_movie: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, index=True)
    synopsis: Optional[str] = Field(default=None, nullable=True)
    release_date: date = Field(nullable=False)
    duration_minutes: int = Field(nullable=False)
    age_rating: Optional[str] = Field(default=None, nullable=True)  # Corrigido: nullable=True
    director: Optional[str] = Field(default=None, nullable=True)    # Corrigido: nullable=True

    # Relações
    reviews: List["Review"] = Relationship(back_populates="movie")
    watchlists: List["Watchlist"] = Relationship(back_populates="movie")
    genres: List["Genre"] = Relationship(back_populates="movies", link_model="MovieGenre")
    actors: List["Actor"] = Relationship(back_populates="movies", link_model="MovieActor")