from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from .review import Review
    from .watchlist import Watchlist
    from .movie_genre import MovieGenre
    from .movie_actor import MovieActor
    from .genre import Genre
    from .actor import Actor

class Movie(SQLModel, table=True):
    id_movie: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    synopsis: Optional[str] = Field(default=None, nullable=True)
    release_date: date = Field(nullable=False)
    duration_minutes: int = Field(default=0, nullable=False)
    age_rating: Optional[str] = Field(default=None, nullable=False)
    director: Optional[str] = Field(default=None, nullable=False)

    reviews: List["Review"] = Relationship(back_populates="movie")
    watchlist_movie: List["Watchlist"] = Relationship(back_populates="movie")
    genres: List["Genre"] = Relationship(back_populates="movies", link_model="MovieGenre")
    actors: List["Actor"] = Relationship(back_populates="movies", link_model="MovieActor")