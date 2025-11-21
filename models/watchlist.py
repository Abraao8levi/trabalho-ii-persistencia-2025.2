from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .movie import Movie

class Watchlist(SQLModel, table=True):
    id_watchlist: Optional[int] = Field(default=None, primary_key=True)
    notes: Optional[str] = Field(default=None, nullable=True)
    id_user: int = Field(foreign_key="user.id_user", nullable=False)
    id_movie: int = Field(foreign_key="movie.id_movie", nullable=False)

    user: "User" = Relationship(back_populates="watchlist")
    movie: "Movie" = Relationship(back_populates="watchlist")